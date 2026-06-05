import json

with open(r"c:\Users\leand\Documents\Projetos\Wild Rift\metadata.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for item_id, item in data["items"].items():
    desc = item.get("description", "")
    if "ataques" in desc:
        # Get the text around 'ataques'
        idx = desc.index("ataques")
        start = max(0, idx - 50)
        end = min(len(desc), idx + 100)
        print(f"ID {item_id} ({item['name']}): ... {desc[start:end]} ...")
