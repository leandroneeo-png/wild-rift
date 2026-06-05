import urllib.request
import json
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

html = urllib.request.urlopen(urllib.request.Request("https://wildlegends.net/tier-list", headers=headers)).read().decode('utf-8', errors='replace')
scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
for script in scripts:
    if '"ShallowReactive"' in script or '"pinia"' in script:
        data = json.loads(script.strip())
        print("Raw data length:", len(data))
        # Let's print all string elements in data that contain dashes
        for i, val in enumerate(data):
            if isinstance(val, str) and "-" in val and len(val) < 50:
                print(f"Index {i}: {val}")
        break
