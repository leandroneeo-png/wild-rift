import urllib.request
import json
import time

FIREBASE_CONFIG = {
    "apiKey": "AIzaSyAJfutv_N-tD4d5I4jvFBBaE4oMO3OoQ2Y",
    "projectId": "wild-rift-533bd"
}

def list_documents():
    url = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_CONFIG['projectId']}/databases/(default)/documents/campeoes?key={FIREBASE_CONFIG['apiKey']}&pageSize=300"
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req) as r:
            body = json.loads(r.read().decode('utf-8'))
            return body.get("documents", [])
    except Exception as e:
        print(f"Erro ao listar documentos: {e}")
        return []

def delete_document(doc_path):
    # doc_path is like "projects/wild-rift-533bd/databases/(default)/documents/campeoes/10001"
    url = f"https://firestore.googleapis.com/v1/{doc_path}?key={FIREBASE_CONFIG['apiKey']}"
    req = urllib.request.Request(url, method='DELETE')
    try:
        with urllib.request.urlopen(req) as r:
            if r.status in [200, 204]:
                print(f"Deletado com sucesso: {doc_path.split('/')[-1]}")
                return True
    except Exception as e:
        print(f"Erro ao deletar {doc_path.split('/')[-1]}: {e}")
    return False

def main():
    print("Iniciando listagem de documentos no Firestore...")
    docs = list_documents()
    print(f"Encontrados {len(docs)} documentos.")
    
    deletados = 0
    for doc in docs:
        name = doc.get("name") # e.g. "projects/wild-rift-533bd/databases/(default)/documents/campeoes/10001"
        if name:
            ok = delete_document(name)
            if ok:
                deletados += 1
            time.sleep(0.05) # evitação de rate limit
            
    print(f"Limpeza concluída! Total deletados: {deletados}")

if __name__ == "__main__":
    main()
