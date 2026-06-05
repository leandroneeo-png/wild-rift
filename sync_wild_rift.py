import urllib.request
import urllib.parse
import json
import time
import os

# =========================================================================
# CONFIGURAÇÃO DO FIREBASE (Chaves de Acesso fornecidas)
# =========================================================================
FIREBASE_CONFIG = {
    "apiKey": "AIzaSyAJfutv_N-tD4d5I4jvFBBaE4oMO3OoQ2Y",
    "projectId": "wild-rift-533bd"
}

# Defina como True para enviar para o Firestore, ou False para enviar para o Realtime Database
USAR_FIRESTORE = True

# =========================================================================
# CONFIGURAÇÃO DE PROXY (Caso seu IP esteja bloqueado / timeout)
# =========================================================================
# Se o seu IP estiver temporariamente bloqueado pela Tencent, você pode definir
# um proxy HTTP/HTTPS aqui para contornar o bloqueio (ex: "http://usuario:senha@ip:porta").
# Se não for usar proxy, deixe como None.
PROXY = None

# URLs das APIs da Tencent
TENCENT_HERO_LIST_URL = "https://apps.game.qq.com/lolm/raider/GetHeroListData.php?callback=jsonpCallback"
TENCENT_HERO_EQUIP_URL = "https://apps.game.qq.com/lolm/raider/GetItemEquipData.php"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://lolm.qq.com/' # Referer essencial para evitar erro 404 da Tencent
}

def fetch_jsonp(url):
    # Configura o proxy na requisição caso esteja definido
    if PROXY:
        proxy_support = urllib.request.ProxyHandler({'http': PROXY, 'https': PROXY})
        opener = urllib.request.build_opener(proxy_support)
    else:
        opener = urllib.request.build_opener()

    req = urllib.request.Request(url, headers=headers)
    try:
        with opener.open(req) as r:
            text = r.read().decode('utf-8', errors='replace')
            # Desembrulha a função callback: jsonpCallback(...)
            json_start = text.find('(')
            json_end = text.rfind(')')
            if json_start != -1 and json_end != -1:
                json_str = text[json_start + 1:json_end]
                return json.loads(json_str)
            return json.loads(text)
    except Exception as e:
        print(f"Erro ao buscar API ({url}): {e}")
        return None

def formatar_campo_firestore(val):
    if isinstance(val, str):
        return {"stringValue": val}
    if isinstance(val, (int, float)):
        return {"doubleValue": val}
    if isinstance(val, bool):
        return {"booleanValue": val}
    if isinstance(val, list):
        return {
            "arrayValue": {
                "values": [formatar_campo_firestore(item) for item in val]
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
                print(f"  [Firestore] {payload['nome']} atualizado com sucesso!")
            else:
                print(f"  [Firestore] Erro status {r.status} para {payload['nome']}")
    except Exception as e:
        print(f"  [Firestore] Erro ao enviar {payload['nome']}: {e}")

def atualizar_realtime_db_rest(dados):
    url = f"https://{FIREBASE_CONFIG['projectId']}-default-rtdb.firebaseio.com/campeoes.json?key={FIREBASE_CONFIG['apiKey']}"
    data = json.dumps(dados, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=data,
        headers={'Content-Type': 'application/json'},
        method='PUT'
    )
    try:
        with urllib.request.urlopen(req) as r:
            if r.status == 200:
                print("[Realtime DB] Sincronização concluída com sucesso!")
            else:
                print(f"[Realtime DB] Erro status {r.status}")
    except Exception as e:
        print(f"[Realtime DB] Erro ao atualizar: {e}")

def calcular_tier(win_rate, pick_rate):
    if win_rate >= 52.5 and pick_rate >= 8.0: return "S+"
    if win_rate >= 51.5 and pick_rate >= 5.0: return "S"
    if win_rate >= 50.0 and pick_rate >= 3.0: return "A"
    if win_rate >= 48.0: return "B"
    return "C"

def main():
    print("Carregando dicionário local (hero_dict.json)...")
    if not os.path.exists("hero_dict.json"):
        print("Erro: Arquivo hero_dict.json não encontrado no diretório atual.")
        return
        
    with open("hero_dict.json", "r", encoding="utf-8") as f:
        dicionario_lista = json.load(f)
        
    # Transforma em dicionário mapeado por ID
    dicionario = {str(h["ID_Chines"]): h for h in dicionario_lista}
    print(f"Dicionário carregado com {len(dicionario)} campeões.")

    print("\nBuscando estatísticas no site chinês...")
    dados_hero_list = fetch_jsonp(TENCENT_HERO_LIST_URL)
    if not dados_hero_list or dados_hero_list.get("status") != 0 or "data" not in dados_hero_list:
        print("Erro: Não foi possível obter dados da Tencent.")
        return
        
    campeoes_chineses = dados_hero_list["data"]
    print(f"Obtidos dados de {len(campeoes_chineses)} campeões.")

    dados_atualizados = {}

    for index, champ in enumerate(campeoes_chineses):
        champ_id = str(champ["heroId"])
        info_traduzida = dicionario.get(champ_id)
        
        if info_traduzida:
            nome_ptbr = info_traduzida["Nome_PTBR"]
            print(f"({index + 1}/{len(campeoes_chineses)}) Processando: {nome_ptbr}...")
            
            # Buscar build recomendada
            build_recomendada = []
            runas_recomendadas = []
            spells_recomendados = []
            
            url_equip = f"{TENCENT_HERO_EQUIP_URL}?heroId={champ_id}&callback=jsonpCallback"
            dados_equip = fetch_jsonp(url_equip)
            
            if dados_equip and dados_equip.get("status") == 0 and "data" in dados_equip:
                equip_list = dados_equip["data"].get("equipList", [])
                if equip_list:
                    primeira_build = equip_list[0]
                    build_recomendada = primeira_build.get("equipItem", [])
                    runas_recomendadas = primeira_build.get("runeId", [])
                    spells_recomendados = primeira_build.get("spellId", [])

            # Calcular tier
            win_rate_val = float(champ["winRate"].replace("%", ""))
            pick_rate_val = float(champ["appearanceRate"].replace("%", ""))
            tier = calcular_tier(win_rate_val, pick_rate_val)

            payload = {
                "id": champ_id,
                "nome": nome_ptbr,
                "slug": info_traduzida["Slug_Url"],
                "winRate": champ["winRate"],
                "pickRate": champ["appearanceRate"],
                "banRate": champ["banRate"],
                "tier": tier,
                "buildRecomendada": build_recomendada,
                "runasRecomendadas": runasRecomendadas,
                "spellsRecomendados": spells_recomendados,
                "atualizadoEm": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }

            if USAR_FIRESTORE:
                atualizar_firestore_rest(champ_id, payload)
            else:
                dados_atualizados[champ_id] = payload
                
            time.sleep(0.15) # Delay amigável para evitar rate limiting

    if not USAR_FIRESTORE:
        print("\nSincronizando todas as informações no Realtime Database...")
        atualizar_realtime_db_rest(dados_atualizados)

    print("\nExecução finalizada!")

if __name__ == "__main__":
    main()
