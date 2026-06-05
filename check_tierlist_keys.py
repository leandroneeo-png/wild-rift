import urllib.request
import json
import re
import sys

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

sys.stdout.reconfigure(encoding='utf-8')

from check_fields import parse_nuxt_state

html = urllib.request.urlopen(urllib.request.Request("https://wildlegends.net/tier-list", headers=headers)).read().decode('utf-8', errors='replace')
state = parse_nuxt_state(html)

if state and 'data' in state:
    tl_data = state['data'].get('tier-list-0', {})
    print("Keys in tier-list-0:", list(tl_data.keys()))
    
    # We also need to map champion names
    # Let's inspect the structure of the items under key '2'
    for k in ['2', '3', '4', '6']:
        if k in tl_data:
            champs = tl_data[k]
            print(f"\n--- Key '{k}' (len={len(champs)}) ---")
            # print names of all champions in this key
            names = [c.get('name') for c in champs]
            print(", ".join(names[:15]) + " ...")
else:
    print("Failed to parse state")
