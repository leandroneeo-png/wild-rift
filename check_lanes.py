import urllib.request
import json
import re
from check_fields import parse_nuxt_state

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

html = urllib.request.urlopen(urllib.request.Request("https://wildlegends.net/ranking", headers=headers)).read().decode('utf-8', errors='replace')
state = parse_nuxt_state(html)
if state:
    mestre = state['pinia']['statistic']['rankList']['1']
    
    with open("hero_dict.json", "r", encoding="utf-8") as f:
        d = json.load(f)
    hero_by_id = {str(h["ID_Chines"]): h["Nome_PTBR"] for h in d}
    
    for lane_key, champs in mestre.items():
        names = [hero_by_id.get(c.get('hero_id'), f"Unknown({c.get('hero_id')})") for c in champs[:5]]
        print(f"Lane Key '{lane_key}': {', '.join(names)}")
else:
    print("Failed to parse state")
