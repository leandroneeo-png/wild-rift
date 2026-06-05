import urllib.request
import json
import time
import os
import re
import sys

# =========================================================================
# CONFIGURAÇÃO DO FIREBASE (Chaves de Acesso fornecidas)
# =========================================================================
FIREBASE_CONFIG = {
    "apiKey": "AIzaSyAJfutv_N-tD4d5I4jvFBBaE4oMO3OoQ2Y",
    "projectId": "wild-rift-533bd"
}

# Caminhos de arquivos locais
HERO_DICT_PATH = "hero_dict.json"
CACHE_FILE_PATH = "builds_cache.json"
METADATA_FILE_PATH = "metadata.json"
metadata = {"items": {}, "runes": {}, "spells": {}}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Fallbacks padrão caso algum guia falhe
FALLBACK_BUILD = ["3078", "3071", "3156", "3026", "3123", "3111"]
FALLBACK_RUNES = ["8009", "8224", "8411", "8306"]
FALLBACK_SPELLS = ["4", "11"]

def fetch_html(url):
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            if r.status == 200:
                return r.read().decode('utf-8', errors='replace')
    except Exception as e:
        print(f"  [Erro] Falha ao baixar URL {url}: {e}")
    return None

def parse_nuxt_state(html):
    # Encontra o script que contém o estado pré-renderizado do Nuxt 3
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
    for script in scripts:
        if '"ShallowReactive"' in script or '"pinia"' in script:
            try:
                data = json.loads(script.strip())
                return decode_nuxt_state(data)
            except Exception as e:
                pass
    return None

def decode_nuxt_state(data):
    """
    Decodifica a estrutura indexada de referências de estado do Nuxt 3/devalue.
    """
    resolved_cache = {}
    
    def get_val(idx):
        if idx in resolved_cache:
            return resolved_cache[idx]
        if not isinstance(idx, int) or idx < 0 or idx >= len(data):
            return idx
            
        raw = data[idx]
        if not isinstance(raw, (dict, list)):
            return raw
            
        if isinstance(raw, list):
            # Resolve invólucros reativos do Vue
            if len(raw) == 2 and isinstance(raw[0], str) and raw[0] in ['ShallowReactive', 'Reactive', 'Ref', 'ShallowRef']:
                res = get_val(raw[1])
                resolved_cache[idx] = res
                return res
            
            res = []
            resolved_cache[idx] = res
            for item in raw:
                if isinstance(item, int):
                    res.append(get_val(item))
                else:
                    res.append(item)
            return res
            
        if isinstance(raw, dict):
            res = {}
            resolved_cache[idx] = res
            for k, v in raw.items():
                if isinstance(v, int):
                    res[k] = get_val(v)
                else:
                    res[k] = v
            return res
            
        return raw

    return get_val(1) # O nó raiz costuma estar no índice 1

def format_description(desc):
    if not desc:
        return ""
    return re.sub(r'src=["\']/icons/', 'src="https://wildlegends.net/icons/', desc)

def normalize_name(name):
    # Remove acentos, espaços e pontuações para correspondência tolerante
    name = name.strip().lower()
    replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'â': 'a', 'ê': 'e', 'î': 'i', 'ô': 'o', 'û': 'u',
        'ç': 'c', ' ': '', '-': '', "'": '', '.': ''
    }
    for k, v in replacements.items():
        name = name.replace(k, v)
    return name

def formatar_campo_firestore(val):
    if isinstance(val, str):
        return {"stringValue": val}
    if isinstance(val, bool):
        return {"booleanValue": val}
    if isinstance(val, int):
        return {"integerValue": str(val)}
    if isinstance(val, float):
        return {"doubleValue": val}
    if isinstance(val, list):
        return {
            "arrayValue": {
                "values": [formatar_campo_firestore(item) for item in val]
            }
        }
    if isinstance(val, dict):
        return {
            "mapValue": {
                "fields": {k: formatar_campo_firestore(v) for k, v in val.items()}
            }
        }
    return {"stringValue": str(val)}

def atualizar_firestore_rest(hero_id, payload):
    url = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_CONFIG['projectId']}/databases/(default)/documents/campeoes/{hero_id}?key={FIREBASE_CONFIG['apiKey']}"
    
    firestore_doc = {"fields": {}}
    for k, v in payload.items():
        firestore_doc["fields"][k] = formatar_campo_firestore(v)
        
    data = json.dumps(firestore_doc).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=data,
        headers={'Content-Type': 'application/json'},
        method='PATCH'
    )
    try:
        with urllib.request.urlopen(req) as r:
            if r.status == 200:
                print(f"  [Firestore] {payload['nome']} enviado com sucesso!")
                return True
            else:
                print(f"  [Firestore] Erro status {r.status} para {payload['nome']}")
    except Exception as e:
        print(f"  [Firestore] Erro ao enviar {payload['nome']}: {e}")
    return False

def calcular_tier(win_rate, pick_rate):
    if win_rate >= 51.5 and pick_rate >= 5.0: return "S"
    if win_rate >= 50.0 and pick_rate >= 3.0: return "A"
    if win_rate >= 48.0: return "B"
    return "C"

def main():
    force_refresh = "--refresh" in sys.argv or "--force" in sys.argv
    print("=== Sincronizador de Estatísticas Wild Rift ===")
    
    # 1. Carregar dicionário local
    print(f"Carregando dicionário local ({HERO_DICT_PATH})...")
    if not os.path.exists(HERO_DICT_PATH):
        print(f"[Erro] Arquivo {HERO_DICT_PATH} não encontrado.")
        return
        
    with open(HERO_DICT_PATH, "r", encoding="utf-8") as f:
        hero_dict_list = json.load(f)
        
    hero_by_name = {normalize_name(h["Nome_PTBR"]): h for h in hero_dict_list}
    print(f"Dicionário carregado com {len(hero_dict_list)} campeões cadastrados.")
    
    # 2. Carregar Cache de Builds
    builds_cache = {}
    if not force_refresh and os.path.exists(CACHE_FILE_PATH):
        try:
            with open(CACHE_FILE_PATH, "r", encoding="utf-8") as f:
                builds_cache = json.load(f)
            print(f"Cache de builds carregado com {len(builds_cache)} campeões.")
        except Exception as e:
            print(f"[Aviso] Erro ao carregar cache de builds, criando novo: {e}")
    else:
        if force_refresh:
            print("Parâmetro de refresh detectado. Cache limpo.")

    # 2b. Carregar metadata acumulado
    global metadata
    if os.path.exists(METADATA_FILE_PATH):
        try:
            with open(METADATA_FILE_PATH, "r", encoding="utf-8") as f:
                metadata = json.load(f)
                if "items" not in metadata: metadata["items"] = {}
                if "runes" not in metadata: metadata["runes"] = {}
                if "spells" not in metadata: metadata["spells"] = {}
            print(f"Metadados acumulados carregados: {len(metadata['items'])} itens, {len(metadata['runes'])} runas, {len(metadata['spells'])} feitiços.")
        except Exception as e:
            print(f"[Aviso] Erro ao carregar metadata.json, criando novo: {e}")

    # 2b-2. Coletar o catálogo completo de itens, runas e feitiços em wildlegends.net/itens
    print("\nColetando catálogo completo de itens e runas em wildlegends.net/itens...")
    itens_html = fetch_html("https://wildlegends.net/itens")
    if itens_html:
        itens_state = parse_nuxt_state(itens_html)
        if itens_state and 'pinia' in itens_state:
            # 1. Carregar todos os itens oficiais do Pinia store do site
            site_items = itens_state['pinia'].get('item', {}).get('items', [])
            for item in site_items:
                item_id = str(item.get("id"))
                desc = format_description(item.get("description", ""))
                metadata["items"][item_id] = {
                    "name": item.get("name"),
                    "description": desc,
                    "price": item.get("price", 0),
                    "imageUrl": item.get("imageUrl") or item.get("image")
                }
            print(f"Catalogados {len(site_items)} itens oficiais da base do Wild Legends.")

            # 2. Carregar todas as runas oficiais do Pinia store do site
            site_runes = itens_state['pinia'].get('rune', {}).get('runes', [])
            for rune in site_runes:
                riot_id = rune.get("riot_id")
                rune_id = str(riot_id) if riot_id else str(rune.get("id"))
                desc = format_description(rune.get("longDesc") or rune.get("shortDesc") or "")
                metadata["runes"][rune_id] = {
                    "name": rune.get("name"),
                    "description": desc,
                    "imageUrl": rune.get("imageUrl") or rune.get("image")
                }
            print(f"Catalogadas {len(site_runes)} runas oficiais da base do Wild Legends.")
            
            # 3. Carregar feitiços (spells) do Pinia store do site se disponível
            site_spells = itens_state['pinia'].get('spell', {}).get('spells', [])
            for spell in site_spells:
                spell_id = str(spell.get("id"))
                metadata["spells"][spell_id] = {
                    "name": spell.get("name"),
                    "description": format_description(spell.get("description", "")),
                    "imageUrl": spell.get("imageUrl") or spell.get("image")
                }
            if site_spells:
                print(f"Catalogados {len(site_spells)} feitiços oficiais da base do Wild Legends.")
        else:
            print("[Aviso] Não foi possível encontrar a store Pinia na página de itens.")
    else:
        print("[Aviso] Falha ao baixar catálogo oficial de itens e runas.")


    # 2c. Baixar a Tier List oficial para cruzar os tiers curados
    print("\nColetando a Tier List oficial em wildlegends.net/tier-list...")
    tierlist_html = fetch_html("https://wildlegends.net/tier-list")
    tier_by_champ_role = {}
    if tierlist_html:
        tierlist_state = parse_nuxt_state(tierlist_html)
        if tierlist_state and 'data' in tierlist_state:
            tl_data = tierlist_state['data'].get('tier-list-0', {})
            # Mapeamento: chave do Nuxt -> Tier
            TIER_MAP = {
                "6": "S",
                "4": "A",
                "3": "B",
                "2": "C"
            }
            for tier_key, champs in tl_data.items():
                if not isinstance(champs, list):
                    continue
                mapped_tier = TIER_MAP.get(str(tier_key), "C")
                for c in champs:
                    c_name = normalize_name(c.get("name", ""))
                    c_role = c.get("role")
                    if c_name and c_role:
                        tier_by_champ_role[(c_name, c_role)] = mapped_tier
            print(f"Mapeados {len(tier_by_champ_role)} campeões da Tier List oficial.")
        else:
            print("[Aviso] Não foi possível decodificar os dados da Tier List oficial.")
    else:
        print("[Aviso] Falha ao baixar a Tier List oficial.")
            
    # 3. Baixar estatísticas do ranking
    print("\nColetando estatísticas globais em wildlegends.net/ranking...")
    ranking_html = fetch_html("https://wildlegends.net/ranking")
    if not ranking_html:
        print("[Erro] Não foi possível acessar o ranking do WildLegends.")
        return
        
    print("Decodificando estado do site...")
    nuxt_state = parse_nuxt_state(ranking_html)
    if not nuxt_state:
        print("[Erro] Falha ao extrair dados do ranking (Nuxt state inválido).")
        return
        
    statistic_store = nuxt_state.get("pinia", {}).get("statistic", {})
    champion_store = nuxt_state.get("pinia", {}).get("champion", {})
    
    # Dicionário do site: hero_id -> alias/pinyin
    hero_list_site = statistic_store.get("heroList", {})
    # Dicionário do site: alias/pinyin -> Nome real
    pinyin_to_name = nuxt_state.get("data", {}).get("champion-name-mappings", {}).get("mappings", {})
    defaults = nuxt_state.get("data", {}).get("champion-name-mappings", {}).get("defaults", {})
    
    # Dicionário de campeões no site para buscar riot_id/slug
    champions_site = champion_store.get("champions", [])
    slug_by_name = {}
    for c in champions_site:
        slug_by_name[c.get("name").lower()] = c.get("riot_id")
        
    # Obtém o ranking do elo Mestre+ (index "1" no rankList)
    rank_list_mestre = statistic_store.get("rankList", {}).get("1", {})
    if not rank_list_mestre:
        print("[Erro] Ranking do elo Mestre+ não encontrado nos dados coletados.")
        return
        
    print("Processando estatísticas extraídas...")
    champions_stats = {}
    
    STRENGTH_TO_TIER = {
        "0": "S",
        "1": "S",
        "2": "A",
        "3": "B",
        "4": "C",
        "5": "D"
    }

    # Roda sobre todas as lanes/posições (1=Mid, 2=Solo, 3=ADC, 4=Suporte, 5=Selva)
    for position_key, champ_list in rank_list_mestre.items():
        if not isinstance(champ_list, list):
            continue
            
        for c in champ_list:
            h_id_str = str(c.get("hero_id"))
            
            # Resolve o alias de pinyin
            hero_info = hero_list_site.get(h_id_str)
            if not hero_info:
                continue
                
            alias = hero_info.get("alias")
            # Encontra o nome real correspondente
            nome_real = pinyin_to_name.get(alias) or defaults.get(alias)
            if not nome_real:
                continue
                
            norm_name = normalize_name(nome_real)
            # Verifica se o campeão está no dicionário local do usuário
            hero_local = hero_by_name.get(norm_name)
            if not hero_local:
                # Ignora campeões novos que não estão em hero_dict.json
                continue
                
            champ_id = str(hero_local["ID_Chines"])
            nome_ptbr = hero_local["Nome_PTBR"]
            slug_url = hero_local["Slug_Url"]
            
            win_rate_str = c.get("win_rate_percent", "50.0") + "%"
            pick_rate_str = c.get("appear_rate_percent", "1.0") + "%"
            ban_rate_str = c.get("forbid_rate_percent", "1.0") + "%"
            
            # Mapeia position_key (1=Mid, 2=Solo, 3=ADC, 4=Suporte, 5=Selva)
            # para o role do Tier List (1=Solo, 2=Jungle, 3=Mid, 4=ADC, 5=Support)
            RANKING_LANE_TO_TIERLIST_ROLE = {
                "1": 3,  # Mid -> Mid
                "2": 1,  # Solo -> Solo
                "3": 4,  # ADC -> ADC
                "4": 5,  # Suporte -> Support
                "5": 2   # Selva -> Jungle
            }
            role_id = RANKING_LANE_TO_TIERLIST_ROLE.get(str(position_key))
            
            # Procura o tier oficial na Tier List curada
            tier = None
            if role_id:
                tier = tier_by_champ_role.get((norm_name, role_id))
            
            # Se não encontrado na Tier List curada, usa fallback baseado no ranking strength_level
            if not tier:
                strength_level = str(c.get("strength_level", "2"))
                tier = STRENGTH_TO_TIER.get(strength_level, "B")
            
            # Variação do ranking (win_rate_float)
            variacao = str(c.get("win_rate_float", "0"))
            
            # Identificador único de documento: {ID do Campeão}_{ID da Rota}
            doc_id = f"{champ_id}_{position_key}"
            
            champions_stats[doc_id] = {
                "id": champ_id,
                "nome": nome_ptbr,
                "slug": slug_url,
                "winRate": win_rate_str,
                "pickRate": pick_rate_str,
                "banRate": ban_rate_str,
                "tier": tier,
                "lane": position_key,
                "variacao": variacao,
                # Chaves auxiliares para o scraping de build
                "_site_name": nome_real,
                "_site_slug": slug_by_name.get(nome_real.lower(), slug_url)
            }

    print(f"Mapeados {len(champions_stats)} registros de campeões por lane ativos com estatísticas do ranking.")
    
    # 4. Baixar builds (itens, runas, spells) com Cache
    print("\nBuscando builds recomendadas (itens, runas, spells)...")
    total_champs = len(champions_stats)
    
    for idx, (doc_id, info) in enumerate(champions_stats.items()):
        name = info["nome"]
        site_slug = info["_site_slug"]
        real_champ_id = info["id"]
        
        # Verifica se já está no cache usando o ID numérico real do campeão e tem as novas chaves
        if not force_refresh and real_champ_id in builds_cache and "skills" in builds_cache[real_champ_id] and "forteContra" in builds_cache[real_champ_id]:
            cache_entry = builds_cache[real_champ_id]
            info["buildRecomendada"] = cache_entry.get("buildRecomendada", FALLBACK_BUILD)
            info["runasRecomendadas"] = cache_entry.get("runasRecomendadas", FALLBACK_RUNES)
            info["spellsRecomendados"] = cache_entry.get("spellsRecomendados", FALLBACK_SPELLS)
            info["skills"] = cache_entry.get("skills", [])
            info["maxingOrder"] = cache_entry.get("maxingOrder", [])
            info["forteContra"] = cache_entry.get("forteContra", [])
            info["fracoContra"] = cache_entry.get("fracoContra", [])
            print(f"({idx+1}/{total_champs}) [Cache] {name} (Lane {info['lane']})")
        else:
            # Caso contrário, faz scrap da página de guia
            print(f"({idx+1}/{total_champs}) [Download] {name} (guia: {site_slug})...")
            guide_url = f"https://wildlegends.net/guia/{site_slug}"
            guide_html = fetch_html(guide_url)
            
            build_recomendada = FALLBACK_BUILD
            runas_recomendadas = FALLBACK_RUNES
            spells_recomendados = FALLBACK_SPELLS
            skills_recomendadas = []
            maxing_order = []
            forte_contra = []
            fraco_contra = []
            
            if guide_html:
                guide_state = parse_nuxt_state(guide_html)
                if guide_state:
                    guides_list = guide_state.get("data", {}).get(f"guides-{site_slug}-0", [])
                    if guides_list and len(guides_list) > 0:
                        first_guide = guides_list[0]
                        
                        # 1. Itens (Type 4 build)
                        guide_builds = first_guide.get("guideBuilds", [])
                        full_build_items = []
                        for build in guide_builds:
                            items_list = build.get("items", [])
                            
                            # Extract metadata for all items in the build
                            for it in items_list:
                                item_obj = it.get("item", {})
                                if item_obj and item_obj.get("id"):
                                    item_id = str(item_obj.get("id"))
                                    metadata["items"][item_id] = {
                                        "name": item_obj.get("name"),
                                        "description": item_obj.get("description", ""),
                                        "imageUrl": item_obj.get("imageUrl")
                                    }
                                    
                            if build.get("type") == 4:
                                full_build_items = [str(it.get("item", {}).get("id")) for it in items_list if it.get("item", {}).get("id")]
                                break
                        if full_build_items:
                            build_recomendada = full_build_items
                            
                        # 2. Runas
                        guide_runes = first_guide.get("guideRunes", [])
                        if guide_runes and len(guide_runes) > 0:
                            rune_items = guide_runes[0].get("items", [])
                            for r in rune_items:
                                r_id = r.get("riot_id") or r.get("id")
                                if r_id:
                                    rune_id = str(r_id)
                                    metadata["runes"][rune_id] = {
                                        "name": r.get("name"),
                                        "description": r.get("longDesc") or r.get("shortDesc") or "",
                                        "imageUrl": r.get("imageUrl")
                                    }
                                    
                            runas_list = [str(r.get("riot_id") or r.get("id")) for r in rune_items if r.get("riot_id") or r.get("id")]
                            if runas_list:
                                runas_recomendadas = runas_list
                                
                        # 3. Spells
                        guide_spells = first_guide.get("guideSpell", {}).get("items", [])
                        for s in guide_spells:
                            spell_obj = s.get("spell", {})
                            if spell_obj and spell_obj.get("id"):
                                spell_id = str(spell_obj.get("id"))
                                metadata["spells"][spell_id] = {
                                    "name": spell_obj.get("name"),
                                    "description": spell_obj.get("description", ""),
                                    "imageUrl": spell_obj.get("imageUrl")
                                }
                                
                        spells_list = [str(s.get("spell", {}).get("id")) for s in guide_spells if s.get("spell", {}).get("id")]
                        if spells_list:
                            spells_recomendados = spells_list

                        # 4. Habilidades e Ordem
                        skills_list = []
                        # Encontra dados do campeão dinamicamente no Nuxt state
                        for k, v in guide_state.get("data", {}).items():
                            if k.startswith("champion-") and isinstance(v, dict) and "skills" in v:
                                skills_list = v.get("skills", [])
                                break
                        if not skills_list:
                            details_cache = guide_state.get("pinia", {}).get("champion", {}).get("detailsCache", {})
                            for slug_key, val in details_cache.items():
                                if isinstance(val, dict) and "data" in val and "skills" in val["data"]:
                                    skills_list = val["data"]["skills"]
                                    break

                        # Extrai upgrades da guia
                        guide_skills_raw = first_guide.get("guideSkill", {}) or {}
                        guide_skills_items = guide_skills_raw.get("items", {}) or {}

                        skills_formatted = []
                        for s in skills_list:
                            s_key = s.get("key")
                            if s_key in ['passive', 'q', 'w', 'e', 'r']:
                                s_id = str(s.get("id"))
                                upgrades = []
                                if s_id in guide_skills_items:
                                    upgrades = [idx + 1 for idx in guide_skills_items[s_id]]
                                skills_formatted.append({
                                    "id": s_id,
                                    "key": s_key,
                                    "name": s.get("name"),
                                    "description": format_description(s.get("description", "")),
                                    "imageUrl": s.get("imageUrl"),
                                    "upgrades": upgrades
                                })
                        skills_recomendadas = skills_formatted

                        # Determina ordem de max (Q, W, E por último upgrade)
                        basic_skills = [s for s in skills_formatted if s["key"] in ['q', 'w', 'e']]
                        basic_skills_with_upgrades = [s for s in basic_skills if s.get("upgrades")]
                        basic_skills_with_upgrades.sort(key=lambda s: s["upgrades"][-1] if len(s["upgrades"]) > 0 else 999)
                        maxing_order = [s["key"] for s in basic_skills_with_upgrades]
                        # 5. Forte Contra / Fraco Contra (Counters)
                        guide_counters = first_guide.get("guideCounters", [])
                        for gc in guide_counters:
                            gc_title = gc.get("title") or ""
                            gc_items = gc.get("items") or []
                            is_forte = "forte" in gc_title.lower() or "strong" in gc_title.lower()
                            is_fraco = "fraco" in gc_title.lower() or "weak" in gc_title.lower()
                            
                            for item in gc_items:
                                c_info = item.get("champion")
                                if c_info:
                                    c_name = c_info.get("name")
                                    c_riot_id = c_info.get("riot_id")
                                    norm_cname = normalize_name(c_name)
                                    
                                    local_c = hero_by_name.get(norm_cname)
                                    if not local_c and c_riot_id:
                                        local_c = hero_by_name.get(normalize_name(c_riot_id))
                                        
                                    if local_c:
                                        c_entry = {
                                            "id": str(local_c["ID_Chines"]),
                                            "nome": local_c["Nome_PTBR"],
                                            "slug": local_c["Slug_Url"]
                                        }
                                    else:
                                        c_entry = {
                                            "id": str(c_info.get("id", "")),
                                            "nome": c_name,
                                            "slug": c_info.get("key", c_name).lower()
                                        }
                                    
                                    if is_forte:
                                        forte_contra.append(c_entry)
                                    elif is_fraco:
                                        fraco_contra.append(c_entry)
            
            info["buildRecomendada"] = build_recomendada
            info["runasRecomendadas"] = runas_recomendadas
            info["spellsRecomendados"] = spells_recomendados
            info["skills"] = skills_recomendadas
            info["maxingOrder"] = maxing_order
            info["forteContra"] = forte_contra
            info["fracoContra"] = fraco_contra
            
            # Atualiza e salva o cache sob o ID real do campeão
            builds_cache[real_champ_id] = {
                "name": name,
                "buildRecomendada": build_recomendada,
                "runasRecomendadas": runas_recomendadas,
                "spellsRecomendados": spells_recomendados,
                "skills": skills_recomendadas,
                "maxingOrder": maxing_order,
                "forteContra": forte_contra,
                "fracoContra": fraco_contra
            }
            with open(CACHE_FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(builds_cache, f, ensure_ascii=False, indent=2)
                
            time.sleep(1.0)

    # 5. Verificação Automática (Sanity Check)
    print("\nIniciando verificação automática de segurança (Sanity Check)...")
    erros = []
    
    # Check 1: Quantidade mínima de campeões
    if len(champions_stats) < 80:
        erros.append(f"Qtd mínima de campeões não atingida. Esperado >= 80, obtido {len(champions_stats)}")
        
    for doc_id, info in champions_stats.items():
        name = info["nome"]
        
        # Check 2: Formatos de taxas
        for field in ["winRate", "pickRate", "banRate"]:
            val_str = info[field]
            if not val_str.endswith("%"):
                erros.append(f"Campeão {name}: Campo {field} '{val_str}' inválido, deve terminar com '%'")
            else:
                try:
                    val_float = float(val_str.replace("%", ""))
                    if field == "winRate" and (val_float < 30.0 or val_float > 70.0):
                        erros.append(f"Campeão {name}: Winrate anormal de {val_float}%")
                    if val_float < 0.0:
                        erros.append(f"Campeão {name}: Taxa negativa {field} de {val_float}%")
                except ValueError:
                    erros.append(f"Campeão {name}: Campo {field} '{val_str}' não pôde ser convertido para número")
                    
        # Check 3: Presença de Builds, Runas e Spells válidos
        if not info["buildRecomendada"] or len(info["buildRecomendada"]) < 1:
            erros.append(f"Campeão {name}: Lista de build recomendada vazia")
        if not info["runasRecomendadas"] or len(info["runasRecomendadas"]) < 1:
            erros.append(f"Campeão {name}: Lista de runas recomendadas vazia")
        if not info["spellsRecomendados"] or len(info["spellsRecomendados"]) < 1:
            erros.append(f"Campeão {name}: Lista de feitiços recomendados vazia")
        if "skills" not in info or not info["skills"] or len(info["skills"]) < 4:
            erros.append(f"Campeão {name}: Lista de habilidades vazia ou incompleta")

    # Avaliação do Sanity Check
    if erros:
        print("\n[FALHA] A verificação automática detectou inconsistências:")
        for e in erros[:10]:
            print(f"  - {e}")
        if len(erros) > 10:
            print(f"  ... e mais {len(erros)-10} erros.")
        print("\n[Abortado] A sincronização no Firestore foi cancelada para proteger os dados atuais.")
        return
        
    print("[SUCESSO] Todos os dados foram verificados com sucesso!")
    
    # 6. Atualização Automática no Firestore
    print("\nIniciando atualização automática no Firestore...")
    sucessos = 0
    falhas = 0
    
    for doc_id, info in champions_stats.items():
        payload = {
            "id": info["id"],
            "nome": info["nome"],
            "slug": info["slug"],
            "winRate": info["winRate"],
            "pickRate": info["pickRate"],
            "banRate": info["banRate"],
            "tier": info["tier"],
            "lane": info["lane"],
            "variacao": info["variacao"],
            "buildRecomendada": info["buildRecomendada"],
            "runasRecomendadas": info["runasRecomendadas"],
            "spellsRecomendados": info["spellsRecomendados"],
            "skills": info.get("skills", []),
            "maxingOrder": info.get("maxingOrder", []),
            "forteContra": info.get("forteContra", []),
            "fracoContra": info.get("fracoContra", []),
            "atualizadoEm": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        
        ok = atualizar_firestore_rest(doc_id, payload)
        if ok:
            sucessos += 1
        else:
            falhas += 1
        time.sleep(0.08) # Pequena pausa entre envios
        
    # 7. Salvar metadados de itens, runas e spells
    print(f"\nSalvando metadados acumulados em {METADATA_FILE_PATH}...")
    print(f"  Itens catalogados: {len(metadata['items'])}")
    print(f"  Runas catalogadas: {len(metadata['runes'])}")
    print(f"  Feitiços catalogados: {len(metadata['spells'])}")
    try:
        with open(METADATA_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        print("[SUCESSO] Metadados salvos com sucesso!")
    except Exception as e:
        print(f"[Erro] Falha ao salvar metadados: {e}")

    print(f"\nSincronização concluída! Sucessos: {sucessos}, Falhas: {falhas}")
    print("Processamento finalizado!")

if __name__ == "__main__":
    main()
