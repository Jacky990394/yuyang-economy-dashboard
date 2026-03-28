import requests
import json
from datetime import datetime

print("啟動昱揚水情偵察機 (最終完美版)...")

# 1. 讀取我們剛剛建好的歷史資料倉庫
with open('water_data.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

# 2. 去水利署 API 抓取「今日即時」數據
api_url = "https://fhy.wra.gov.tw/WraApi/v1/Reservoir/RealTimeInfo"
try:
    response = requests.get(api_url)
    live_data = response.json()
    
    # 鎖定三大工業/科學園區水庫：寶二(30502), 石門(20101), 曾文(30802)
    target_ids = ["30502", "20101", "30802"]
    total_rate = 0
    count = 0
    
    for item in live_data:
        station_no = str(item.get('StationNo', '')) 
        if station_no in target_ids:
            # 🎯 關鍵修正：換成政府現在正確的標籤名稱！
            rate = item.get('PercentageOfStorage', 0) 
            
            if rate is not None:
                # 幫抓下來的落落長小數點做四捨五入，保留1位
                rate_rounded = round(float(rate), 1)
                print(f"📍 找到目標水庫代碼 {station_no}，真實蓄水率：{rate_rounded}%")
                total_rate += rate_rounded
                count += 1
            
    # 算出今天最新的平均蓄水率
    today_avg = round(total_rate / count, 1) if count > 0 else 0
    print(f"\n✅ 成功計算！今日三大水庫平均蓄水率：{today_avg}%")

    # 3. 判斷燈號
    warning_level = "綠燈 (水源充足)"
    if today_avg < 30:
        warning_level = "紅燈 (警戒 - 限水危機)"
    elif today_avg < 60:
        warning_level = "黃燈 (吃緊 - 預警中)"

    # 4. 更新資料倉庫
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db["update_time"] = now_str
    db["overall_warning_level"] = warning_level
    db["average_storage_rate"] = today_avg
    db["history_data"][-1] = today_avg

    # 5. 將更新後的資料寫回 JSON 檔案
    with open('water_data.json', 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
        
    print(f"📁 資料已成功寫入 water_data.json，更新時間：{now_str}\n")

except Exception as e:
    print(f"❌ 抓取失敗: {e}")