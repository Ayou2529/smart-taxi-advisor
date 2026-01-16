import requests
import json
from datetime import datetime, timedelta
import time
import random

# ================= CONFIGURATION =================
# ใส่ Line Notify Token ของคุณที่นี่ (สมัครได้ที่ notify-bot.line.me)
LINE_NOTIFY_TOKEN = "YOUR_LINE_TOKEN_HERE"

# ใส่ AviationStack API Key ของคุณที่นี่ (สมัครฟรีที่ aviationstack.com)
# ถ้าไม่มีคีย์ ให้ตั้งค่า USE_DEMO_DATA = True เพื่อทดสอบระบบด้วยข้อมูลจำลอง
AVIATION_STACK_API_KEY = "YOUR_API_KEY_HERE"
USE_DEMO_DATA = True  # เปลี่ยนเป็น False เมื่อมี API Key แล้ว

# สนามบินที่ต้องการเช็ค (BKK = สุวรรณภูมิ, DMK = ดอนเมือง)
AIRPORT_CODE = "BKK" 
# =================================================

def get_flight_data_demo():
    """
    สร้างข้อมูลเที่ยวบินจำลองสำหรับการทดสอบ
    """
    print("⚠️ กำลังใช้โหมด Demo (จำลองข้อมูล)...")
    airlines = ["Emirates", "Qatar Airways", "Thai Airways", "China Eastern", "Lufthansa", "EVA Air", "Spring Airlines", "IndiGo"]
    origins = ["London", "Dubai", "Frankfurt", "Tokyo", "Shanghai", "Singapore", "Mumbai", "Beijing"]
    
    mock_flights = []
    # สุ่มสร้าง 15-25 เที่ยวบิน
    for _ in range(random.randint(15, 25)):
        flight = {
            "airline": random.choice(airlines),
            "flight_number": f"{random.choice(['TG', 'EK', 'QR', 'LH', '9C', '6E'])}{random.randint(100, 999)}",
            "origin": random.choice(origins),
            "arrival_time": datetime.now().strftime("%H:%M")
        }
        mock_flights.append(flight)
    return mock_flights

def get_flight_data_real():
    """
    ดึงข้อมูลจริงจาก AviationStack API
    """
    if not AVIATION_STACK_API_KEY or AVIATION_STACK_API_KEY == "YOUR_API_KEY_HERE":
        print("❌ Error: ยังไม่ได้ใส่ API Key")
        return []

    url = "http://api.aviationstack.com/v1/flights"
    params = {
        'access_key': AVIATION_STACK_API_KEY,
        'arr_iata': AIRPORT_CODE,
        'flight_status': 'landed' # หรือ 'scheduled' สำหรับอนาคต
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'data' not in data:
            return []

        flights = []
        for item in data['data']:
            flight = {
                "airline": item['airline']['name'],
                "flight_number": item['flight']['iata'],
                "origin": item['departure']['airport'],
                "arrival_time": item['arrival']['scheduled'].split('T')[-1][:5] # เอาแค่เวลา HH:MM
            }
            flights.append(flight)
        return flights
    except Exception as e:
        print(f"❌ Error API: {e}")
        return []

def send_line_notify(message):
    """
    ส่งข้อความแจ้งเตือนผ่าน Line Notify
    """
    if LINE_NOTIFY_TOKEN == "YOUR_LINE_TOKEN_HERE":
        print("⚠️ ยังไม่ได้ใส่ Line Token (ข้อความจะแสดงแค่ในจอนี้)")
        print(f"💬 ข้อความที่จะส่ง: {message}")
        return

    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {LINE_NOTIFY_TOKEN}"}
    data = {"message": message}
    
    try:
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            print("✅ ส่ง Line เรียบร้อย!")
        else:
            print(f"❌ ส่ง Line ไม่สำเร็จ: {response.status_code}")
    except Exception as e:
        print(f"❌ Error Line: {e}")

def analyze_and_notify():
    print(f"✈️ กำลังเช็คข้อมูลเที่ยวบินขาเข้าสนามบิน {AIRPORT_CODE}...")
    
    if USE_DEMO_DATA:
        flights = get_flight_data_demo()
    else:
        flights = get_flight_data_real()
        
    count = len(flights)
    print(f"พบ {count} เที่ยวบินในช่วงนี้")

    # ================= ALGORITHM: "Golden Window" & "Fare Estimator" =================
    # ข้อมูล Profiling แยกตามโซนประเทศ (สถิติจากพฤติกรรมนักท่องเที่ยว)
    FLIGHT_PROFILE = {
        "Europe": {
            "hubs": ["London", "Frankfurt", "Paris", "Zurich", "Munich", "Amsterdam", "Helsinki", "Copenhagen"],
            "exit_delay": 50,  # นานที่รอกระเป๋า + ไม่ต้องทำ Visa
            "fare_range": "500-800", # ปรับปี 2569: ค่าโดยสาร + ทางด่วน + ทิป
            "comment": "กระเป๋าเยอะ เข้าเมืองไกล (สุขุมวิท/สีลม)"
        },
        "MiddleEast": {
            "hubs": ["Dubai", "Doha", "Abu Dhabi", "Istanbul", "Tel Aviv", "Riyadh", "Kuwait"],
            "exit_delay": 60, 
            "fare_range": "450-650", # ปรับขึ้นเล็กน้อย
            "comment": "มาเป็นครอบครัวใหญ่ ทิปหนัก (โซนนานา)"
        },
        "Russia": {
            "hubs": ["Moscow", "Saint Petersburg", "Novosibirsk"],
            "exit_delay": 55,
            "fare_range": "500-1500", # เพิ่มโอกาสเหมาพัทยา
            "comment": "โอกาสเหมาไปพัทยา/หัวหินสูงมาก"
        },
        "EastAsia": {
            "hubs": ["Tokyo", "Osaka", "Seoul", "Taipei"],
            "exit_delay": 45, 
            "fare_range": "400-550", # ปรับฐานขึ้นตาม Grab 2569
            "comment": "สุภาพ จ่ายตรง (แต่อาจจะใช้ App เรียกรถ)"
        },
        "China": {
            "hubs": ["Shanghai", "Beijing", "Guangzhou", "Chengdu", "Kunming"],
            "exit_delay": 75, # VOA คิวยาว
            "fare_range": "350-500", 
            "comment": "ระวัง! รอนานตรวจวีซ่า (ไปโซนรัชดา)"
        },
        "India": {
            "hubs": ["Delhi", "Mumbai", "Kolkata", "Bangalore"],
            "exit_delay": 70, 
            "fare_range": "350-500", 
            "comment": "ไปโซนประตูน้ำ/พาหุรัด"
        }
    }

    smart_alerts = [] # เก็บรายการแจ้งเตือนแบบรายละเอียด

    for f in flights:
        origin = f['origin']
        arrival_time_str = f['arrival_time'] # คาดว่า format 18:30 หรือ T18:30:00
        if 'T' in arrival_time_str:
             arrival_time_str = arrival_time_str.split('T')[-1][:5]
        
        # 1. Match Region
        matched_zone = "Other"
        profile = None
        
        for zone, data in FLIGHT_PROFILE.items():
            if any(hub in origin for hub in data['hubs']):
                matched_zone = zone
                profile = data
                break
        
        # ถ้าเจอโซนเป้าหมาย ให้คำนวณละเอียด
        if profile:
            # 2. Calculate "Golden Window" (เวลาคนออกมาจริงๆ)
            try:
                h, m = map(int, arrival_time_str.split(':'))
                total_mins = h * 60 + m + profile['exit_delay']
                
                # แปลงกลับเป็นเวลาคนออก (Exit Time)
                exit_h = (total_mins // 60) % 24
                exit_m = total_mins % 60
                exit_time_str = f"{exit_h:02}:{exit_m:02}"
                
                # บันทึกข้อมูล
                smart_alerts.append({
                    "airline": f['airline'],
                    "flight": f['flight_number'],
                    "origin": origin,
                    "land_time": arrival_time_str,
                    "exit_time": exit_time_str,
                    "fare": profile['fare_range'],
                    "note": profile['comment'],
                    "zone": matched_zone
                })
            except Exception as e:
                print(f"Error parsing time {arrival_time_str}: {e}")

    # ================= สร้างข้อความแจ้งเตือน (Smart Report) =================
    if len(smart_alerts) > 0:
        # Sort ตามเวลาคนออก (Exit Time) เพื่อให้คนขับรู้ลำดับ
        smart_alerts.sort(key=lambda x: x['exit_time'])
        
        message = (
            f"\n🧠 Smart Advisor: วิเคราะห์เวลารับงาน\n"
            f"📍 สนามบิน: {AIRPORT_CODE}\n"
            f"💰 พบลูกค้าเกรด A+ ทั้งหมด {len(smart_alerts)} ลำ\n"
            f"-------------------------------\n"
        )
        
        for item in smart_alerts[:7]: # ยกมา 7 อันดับแรก
            icon = "💶" if item['zone'] == "Europe" else ("🛢️" if item['zone'] == "MiddleEast" else "🌏")
            message += (
                f"{icon} {item['airline']} ({item['origin']})\n"
                f"   🛬 ลง: {item['land_time']} --> 🚶‍♂️ออก: {item['exit_time']}\n"
                f"   💸 คาดการณ์: {item['fare']}฿\n"
                f"   💡 {item['note']}\n"
            )
            message += "-------------------------------\n"
            
        message += "\nกลยุทธ์แนะนำ:\n"
        first_exit = smart_alerts[0]['exit_time']
        message += f"🚀 ออกรถเลย! เพื่อไปถึงหน้างานตอน {first_exit}\n"
        message += "ลูกค้าจะเริ่มทะลักออกมาพอดี ท่านจะได้คิวแรกๆ ของรอบนี้!"
        
        # เพิ่ม Link MAP
        if AIRPORT_CODE == "BKK":
            map_link = "https://www.google.com/maps/@13.690,100.750,14z/data=!5m1!1e1" 
        else:
            map_link = "https://www.google.com/maps/@13.913,100.604,14z/data=!5m1!1e1" 
        message += f"\n\n🚦 เช็คจราจร:\n{map_link}"
        
        send_line_notify(message)
        
    elif count > 0:
        # กรณีไม่เจอ High Value เลย แต่มีไฟล์ททั่วไป
        send_line_notify(f"🤖 มีเที่ยวบิน {count} ลำ แต่เป็นระยะสั้น (Low Fare) อาจจะไม่คุ้มรอ หรือเน้นรับไวครับ")
    
    else:
        print("เงียบกริบ ไม่มีเครื่องลง")

if __name__ == "__main__":
    analyze_and_notify()
