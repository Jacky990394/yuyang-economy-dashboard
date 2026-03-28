import requests
import json
from datetime import datetime
import urllib3

# 關閉 SSL 警告 (政府網站的憑證有時候會過期)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("啟動昱揚電力偵察機 (能源署備用版)...")

# 1. 讀取歷史資料倉庫
with open('power_data.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

# 2. 改去「經濟部能源署」的開放資料平台抓取台電備轉容量
# 這是另一個穩定的 API 來源
api_url = "https://www.moeaea.gov.tw/ECW/populace/opendata/wrm16/ReserveCapacity.json"

try:
    # 加上 verify=False 避免政府網站憑證問題導致抓不到
    response = requests.get(api_url, verify=False, timeout=10)
    live_data = response.json()
    
    # 印出情報監視器
    print("\n🔍 【情報分析】能源署原始資料 (取第一筆)：")
    if isinstance(live_data, list) and len(live_data) > 0:
        print(json.dumps(live_data[0], indent=2, ensure_ascii=False))
        print("-" * 50)
        
        # 能源署的資料結構通常是一個列表，第一筆就是最新資料
        # 他們的標籤通常是 "ReserveCapacityRate" (備轉容量率)
        latest_data = live_data[0]
        reserve_rate_str = latest_data.get("ReserveCapacityRate", "0")
        reserve_rate = float(reserve_rate_str)
        
        print(f"✅ 成功抓取！今日預估備轉容量率：{reserve_rate}%")

        # 3. 判斷燈號 (台電標準：>10%綠燈，6~10%黃燈，<6%紅燈)
        warning_level = "綠燈 (供電充裕)"
        if reserve_rate <= 6:
            warning_level = "紅燈 (供電警戒 - 廠辦限電風險)"
        elif reserve_rate <= 10:
            warning_level = "黃燈 (供電吃緊)"

        # 4. 更新資料倉庫
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db["update_time"] = now_str
        db["overall_warning_level"] = warning_level
        db["average_reserve_rate"] = reserve_rate
        db["history_data"][-1] = reserve_rate 

        # 5. 寫回 JSON 檔案
        with open('power_data.json', 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
            
        print(f"📁 資料已成功寫入 power_data.json，更新時間：{now_str}\n")
    else:
         print("❌ 抓取失敗: 能源署回傳的資料格式非預期或為空。")

except Exception as e:
    print(f"❌ 電力抓取失敗: {e}")