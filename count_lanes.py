import urllib.request
import json
from sync_wildlegends import FIREBASE_CONFIG

url = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_CONFIG['projectId']}/databases/(default)/documents/campeoes?key={FIREBASE_CONFIG['apiKey']}&pageSize=300"
req = urllib.request.Request(url)
with urllib.request.urlopen(req) as r:
    body = json.loads(r.read().decode('utf-8'))
    docs = body.get("documents", [])
    
    lanes = {}
    for doc in docs:
        lane = doc["fields"]["lane"]["stringValue"]
        lanes[lane] = lanes.get(lane, 0) + 1
        
    print("Firestore documents per lane:")
    for lane, count in sorted(lanes.items()):
        print(f"  Lane {lane}: {count} documents")
