import json
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("啟動【鋼鐵原物料雙指標】偵察機...")

targets = [
    {"file": "iron_ore_data.json", "val": 115.5, "name": "【國際】鐵礦砂"},
    {"file": "csc_steel_data.json", "val": 21000, "name": "【台灣】中鋼熱軋"}
]

now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for t in targets:
    try:
        with open(t["file"], 'r', encoding='utf-8') as f:
            db = json.load(f)
            
        db["update_time"] = now_str
        db["current_value"] = str(t["val"])
        db["history_data"][-1] = t["val"]
        
        with open(t["file"], 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
            
        print(f"✅ {t['name']}已更新：{t['val']}")
    except Exception as e:
        print(f"❌ {t['name']}更新失敗: {e}")

print("📁 鋼鐵關聯資料庫更新完畢！\n")