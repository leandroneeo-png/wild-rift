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
    # 3 is ADC lane
    champs = state['pinia']['statistic']['rankList']['1']['3']
    # Sort by win_rate_percent descending
    champs_sorted = sorted(champs, key=lambda c: float(c.get('win_rate_percent', 0)), reverse=True)
    
    # Load hero_dict to map names
    with open("hero_dict.json", "r", encoding="utf-8") as f:
        d = json.load(f)
    hero_by_id = {str(h["ID_Chines"]): h["Nome_PTBR"] for h in d}
    
    for i, c in enumerate(champs_sorted[:8]):
        name = hero_by_id.get(c.get('hero_id'), 'Unknown')
        print(f"#{i+1} {name} (ID: {c.get('hero_id')}): WR: {c.get('win_rate_percent')}%, PR: {c.get('appear_rate_percent')}%, BR: {c.get('forbid_rate_percent')}%, Float: {c.get('win_rate_float')}")
else:
    print("Failed to parse state")
