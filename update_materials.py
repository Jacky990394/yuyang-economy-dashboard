import json
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("啟動【四大營造材料】偵察機...")

materials = [
    {"file": "pvc_data.json", "val": 28.5, "name": "【台灣】台塑 PVC"},
    {"file": "copper_data.json", "val": 8950, "name": "【國際】LME 銅"},
    {"file": "concrete_data.json", "val": 3200, "name": "【台灣】預拌混凝土"},
    {"file": "asphalt_data.json", "val": 18500, "name": "【台灣】進口瀝青"}
]

now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for m in materials:
    try:
        with open(m["file"], 'r', encoding='utf-8') as f:
            db = json.load(f)
            
        db["update_time"] = now_str
        db["current_value"] = str(m["val"])
        db["history_data"][-1] = m["val"]
        
        with open(m["file"], 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
            
        print(f"✅ {m['name']}已更新：{m['val']}")
    except Exception as e:
        print(f"❌ {m['name']}更新失敗: {e}")

print("📁 營造材料資料庫更新完畢！\n")