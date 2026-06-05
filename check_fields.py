import urllib.request
import json
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def parse_nuxt_state(html):
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
    return get_val(1)

if __name__ == '__main__':
    html = urllib.request.urlopen(urllib.request.Request("https://wildlegends.net/ranking", headers=headers)).read().decode('utf-8', errors='replace')
    state = parse_nuxt_state(html)
    if state:
        rank_list = state.get("pinia", {}).get("statistic", {}).get("rankList", {})
        # Get first list in elo "1"
        mestre = rank_list.get("1", {})
        for lane, champs in mestre.items():
            if champs:
                print("Keys in champion rank entry:", list(champs[0].keys()))
                print("Sample entry:", champs[0])
                break
    else:
        print("Failed to parse state")
