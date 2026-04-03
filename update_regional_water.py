import json
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("啟動【北中南民生水庫】三合一偵察機...")

# 定義要更新的檔案清單與模擬抓取的最新數據 (實務上這裡會呼叫水利署 API)
regions = [
    {"file": "water_north_data.json", "latest_val": 78.5, "name": "北部"},
    {"file": "water_central_data.json", "latest_val": 45.2, "name": "中部"},
    {"file": "water_south_data.json", "latest_val": 24.9, "name": "南部"}
]

now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for region in regions:
    try:
        with open(region["file"], 'r', encoding='utf-8') as f:
            db = json.load(f)
            
        # 更新數值與時間
        db["update_time"] = now_str
        db["current_value"] = str(region["latest_val"])
        db["history_data"][-1] = region["latest_val"]
        
        with open(region["file"], 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
            
        print(f"✅ {region['name']}水情已更新：{region['latest_val']}%")
    except Exception as e:
        print(f"❌ {region['name']}水情更新失敗: {e}")

print("📁 三大水情資料庫更新完畢！\n")