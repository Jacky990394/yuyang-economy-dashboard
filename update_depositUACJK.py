import json
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("啟動【UACJK 跨國定存利率】五合一偵察機...")

# 定義要更新的 5 國檔案與模擬最新利率 (實務上需對接各國央行或財經 API)
nations = [
    {"file": "depositUACJK_US.json", "val": 3.5, "name": "美國"},
    {"file": "depositUACJK_AU.json", "val": 3.1, "name": "澳洲"},
    {"file": "depositUACJK_CN.json", "val": 1.15, "name": "中國"},
    {"file": "depositUACJK_JP.json", "val": 0.025, "name": "日本"},
    {"file": "depositUACJK_KR.json", "val": 2.5, "name": "韓國"}
]

now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for n in nations:
    try:
        with open(n["file"], 'r', encoding='utf-8') as f:
            db = json.load(f)
            
        db["update_time"] = now_str
        db["current_value"] = str(n["val"])
        db["history_data"][-1] = n["val"]
        
        with open(n["file"], 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
            
        print(f"✅ {n['name']}利率已更新：{n['val']}%")
    except Exception as e:
        print(f"❌ {n['name']}利率更新失敗: {e}")

print("📁 UACJK 五大國利率資料庫更新完畢！\n")