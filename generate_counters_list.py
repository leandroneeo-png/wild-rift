import json
import os

def main():
    cache_path = "builds_cache.json"
    output_path = "campeoes_counters.md"

    if not os.path.exists(cache_path):
        print(f"Erro: Arquivo {cache_path} não encontrado!")
        return

    print(f"Lendo {cache_path}...")
    with open(cache_path, "r", encoding="utf-8") as f:
        cache_data = json.load(f)

    # Lista para armazenar dados de cada campeão
    campeoes_lista = []

    for champ_id, champ_data in cache_data.items():
        name = champ_data.get("name", "").strip()
        if not name:
            continue

        forte = champ_data.get("forteContra", [])
        fraco = champ_data.get("fracoContra", [])

        # Extrai os nomes dos counters
        forte_nomes = [c.get("nome", "") for c in forte]
        fraco_nomes = [c.get("nome", "") for c in fraco]

        # Limpa strings vazias e preenche com "Nenhum" ou "-" se vazio
        forte_str = ", ".join(filter(None, forte_nomes)) or "Nenhum"
        fraco_str = ", ".join(filter(None, fraco_nomes)) or "Nenhum"

        campeoes_lista.append({
            "nome": name,
            "forte": forte_str,
            "fraco": fraco_str
        })

    # Ordena alfabeticamente pelo nome do campeão
    campeoes_lista.sort(key=lambda x: x["nome"].lower())

    print(f"Gerando relatório {output_path}...")
    with open(output_path, "w", encoding="utf-8") as out:
        out.write("# Lista de Campeões e seus Counters (Pesquisa)\n\n")
        out.write("Esta lista foi gerada automaticamente a partir dos dados do WildLegends. ")
        out.write("Ela apresenta os 3 campeões contra os quais cada personagem é forte, ")
        out.write("e os 3 campeões contra os quais ele é mais fraco.\n\n")
        
        # Tabela Markdown
        out.write("| Campeão | Forte Contra (Vence) | Fraco Contra (Perde) |\n")
        out.write("| :--- | :--- | :--- |\n")
        
        for c in campeoes_lista:
            out.write(f"| **{c['nome']}** | {c['forte']} | {c['fraco']} |\n")

    print(f"Sucesso! {len(campeoes_lista)} campeões processados e salvos em '{output_path}'.")

if __name__ == "__main__":
    main()
