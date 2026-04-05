import json
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("啟動【營建廢棄物處理】偵察機...")

target = {"file": "waste_disposal_data.json", "val": 145.2, "name": "【台灣】營建廢棄物處理"}
now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

try:
    with open(target["file"], 'r', encoding='utf-8') as f:
        db = json.load(f)
        
    db["update_time"] = now_str
    db["current_value"] = str(target["val"])
    db["history_data"][-1] = target["val"]
    
    with open(target["file"], 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
        
    print(f"✅ {target['name']}已更新：{target['val']}")
except Exception as e:
    print(f"❌ {target['name']}更新失敗: {e}")