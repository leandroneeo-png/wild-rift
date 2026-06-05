import json
import time
import os
import urllib.request

# =========================================================================
# CONFIGURAÇÃO DO FIREBASE
# =========================================================================
FIREBASE_CONFIG = {
    "apiKey": "AIzaSyAJfutv_N-tD4d5I4jvFBBaE4oMO3OoQ2Y",
    "projectId": "wild-rift-533bd"
}

# Defina como True para enviar para o Firestore, ou False para o Realtime Database
USAR_FIRESTORE = True

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
        print("Erro: Arquivo hero_dict.json não encontrado.")
        return
        
    with open("hero_dict.json", "r", encoding="utf-8") as f:
        dicionario_lista = json.load(f)
        
    dicionario = {str(h["ID_Chines"]): h for h in dicionario_lista}
    
    print("Carregando dados locais do arquivo tencent_data.json...")
    if not os.path.exists("tencent_data.json"):
        print("Erro: Arquivo tencent_data.json não encontrado.")
        return
        
    with open("tencent_data.json", "r", encoding="utf-8") as f:
        raw_text = f.read().strip()
        
    # Se o texto começar com a função jsonpCallback(...), desembrulha
    if raw_text.startswith("jsonpCallback"):
        json_start = raw_text.find('(')
        json_end = raw_text.rfind(')')
        if json_start != -1 and json_end != -1:
            raw_text = raw_text[json_start + 1:json_end]
            
    dados_tencent = json.loads(raw_text)
    campeoes_chineses = dados_tencent.get("data", [])
    
    print(f"Lidos dados de {len(campeoes_chineses)} campeões do arquivo local.")
    dados_atualizados = {}

    for index, champ in enumerate(campeoes_chineses):
        champ_id = str(champ["heroId"])
        info_traduzida = dicionario.get(champ_id)
        
        if info_traduzida:
            nome_ptbr = info_traduzida["Nome_PTBR"]
            print(f"({index + 1}/{len(campeoes_chineses)}) Enviando: {nome_ptbr}...")
            
            # Formata estatísticas
            win_rate_str = champ.get("winRate", "50.00%")
            pick_rate_str = champ.get("appearanceRate", "5.00%")
            ban_rate_str = champ.get("banRate", "1.00%")
            
            win_rate_val = float(win_rate_str.replace("%", ""))
            pick_rate_val = float(pick_rate_str.replace("%", ""))
            tier = calcular_tier(win_rate_val, pick_rate_val)
            
            # Pega build mockada ou real caso disponível
            build_recomendada = champ.get("buildRecomendada", ["3078", "3071", "3156", "3026", "3123", "3111"])
            runas_recomendadas = champ.get("runasRecomendadas", ["8009", "8224", "8411", "8306"])
            spells_recomendados = champ.get("spellsRecomendados", ["4", "11"])

            payload = {
                "id": champ_id,
                "nome": nome_ptbr,
                "slug": info_traduzida["Slug_Url"],
                "winRate": win_rate_str,
                "pickRate": pick_rate_str,
                "banRate": ban_rate_str,
                "tier": tier,
                "buildRecomendada": build_recomendada,
                "runasRecomendadas": runas_recomendadas,
                "spellsRecomendados": spells_recomendados,
                "atualizadoEm": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }

            if USAR_FIRESTORE:
                atualizar_firestore_rest(champ_id, payload)
                time.sleep(0.08) # Pequena pausa para evitar sobrecarga
            else:
                dados_atualizados[champ_id] = payload

    if not USAR_FIRESTORE:
        atualizar_realtime_db_rest(dados_atualizados)
        
    print("\nExecução finalizada com sucesso!")

if __name__ == "__main__":
    main()
