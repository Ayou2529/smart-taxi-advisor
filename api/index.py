from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
import random
import requests
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

# Vercel structure: this file is in api/ folder, templates/static are in root
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app = Flask(__name__, 
            template_folder=base_dir, 
            static_folder=os.path.join(base_dir, 'static'))

application = app  # Alias for Vercel/WSGI compatibility

# ================= CONFIGURATION =================
LINE_NOTIFY_TOKEN = os.environ.get("LINE_NOTIFY_TOKEN")
AVIATION_STACK_API_KEY = os.environ.get("AVIATION_STACK_API_KEY")
NOSTRA_API_KEY = os.environ.get("NOSTRA_API_KEY")
FACEBOOK_ACCESS_TOKEN = os.environ.get("FACEBOOK_ACCESS_TOKEN")
USE_DEMO_DATA = os.environ.get("USE_DEMO_DATA", "True").lower() == "true"
AIRPORT_CODE = os.environ.get("AIRPORT_CODE", "BKK")
# =================================================

# ================= CACHING SYSTEM =================
CACHE = {
    "flights": {"data": None, "expires": None},
    "traffic": {"data": None, "expires": None},
    "news": {"data": None, "expires": None}
}
CACHE_DURATION_MINUTES = 10
API_CALL_COUNT = {"flights": 0, "traffic": 0, "news": 0}

def get_cached(key):
    if CACHE[key]["data"] and CACHE[key]["expires"]:
        if datetime.now() < CACHE[key]["expires"]:
            return CACHE[key]["data"]
    return None

def set_cache(key, data):
    CACHE[key]["data"] = data
    CACHE[key]["expires"] = datetime.now() + timedelta(minutes=CACHE_DURATION_MINUTES)
    API_CALL_COUNT[key] += 1
# =================================================

FLIGHT_PROFILE = {
    "Europe": {
        "hubs": ["London", "Frankfurt", "Paris", "Zurich", "Munich", "Amsterdam", "Helsinki", "Copenhagen"],
        "exit_delay": 50,
        "fare_range": "500-800",
        "comment": "กระเป๋าเยอะ เข้าเมืองไกล (สุขุมวิท/สีลม)",
        "icon": "💶",
        "color": "#3B82F6"
    },
    "MiddleEast": {
        "hubs": ["Dubai", "Doha", "Abu Dhabi", "Istanbul", "Tel Aviv", "Riyadh", "Kuwait"],
        "exit_delay": 60,
        "fare_range": "450-650",
        "comment": "มาเป็นครอบครัวใหญ่ ทิปหนัก (โซนนานา)",
        "icon": "🛢️",
        "color": "#F59E0B"
    },
    "Russia": {
        "hubs": ["Moscow", "Saint Petersburg", "Novosibirsk"],
        "exit_delay": 55,
        "fare_range": "500-1500",
        "comment": "โอกาสเหมาไปพัทยา/หัวหินสูงมาก",
        "icon": "🇷🇺",
        "color": "#EF4444"
    },
    "EastAsia": {
        "hubs": ["Tokyo", "Osaka", "Seoul", "Taipei"],
        "exit_delay": 45,
        "fare_range": "400-550",
        "comment": "สุภาพ จ่ายตรง (แต่อาจจะใช้ App เรียกรถ)",
        "icon": "🇯🇵",
        "color": "#EC4899"
    },
    "China": {
        "hubs": ["Shanghai", "Beijing", "Guangzhou", "Chengdu", "Kunming"],
        "exit_delay": 75,
        "fare_range": "350-500",
        "comment": "ระวัง! รอนานตรวจวีซ่า (ไปโซนรัชดา)",
        "icon": "🇨🇳",
        "color": "#F97316"
    },
    "India": {
        "hubs": ["Delhi", "Mumbai", "Kolkata", "Bangalore"],
        "exit_delay": 70,
        "fare_range": "350-500",
        "comment": "ไปโซนประตูน้ำ/พาหุรัด",
        "icon": "🇮🇳",
        "color": "#22C55E"
    }
}

def get_flight_data_demo():
    airlines = ["Emirates", "Qatar Airways", "Thai Airways", "China Eastern", "Lufthansa", "EVA Air", "Spring Airlines", "IndiGo", "ANA", "Korean Air"]
    origins = ["London", "Dubai", "Frankfurt", "Tokyo", "Shanghai", "Singapore", "Mumbai", "Beijing", "Seoul", "Moscow"]
    mock_flights = []
    base_hour = datetime.now().hour
    for i in range(random.randint(12, 20)):
        hour = (base_hour + random.randint(0, 2)) % 24
        minute = random.randint(0, 59)
        flight = {
            "airline": random.choice(airlines),
            "flight_number": f"{random.choice(['TG', 'EK', 'QR', 'LH', '9C', '6E', 'NH', 'KE'])}{random.randint(100, 999)}",
            "origin": random.choice(origins),
            "arrival_time": f"{hour:02}:{minute:02}"
        }
        mock_flights.append(flight)
    return mock_flights

def get_flight_data_real():
    cached = get_cached("flights")
    if cached: return cached
    try:
        url = "http://api.aviationstack.com/v1/flights"
        params = {'access_key': AVIATION_STACK_API_KEY, 'arr_iata': AIRPORT_CODE, 'flight_status': 'active', 'limit': 20}
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        if 'error' in data: return get_flight_data_demo()
        real_flights = []
        if 'data' in data:
            for f in data['data']:
                try:
                    flight = {
                        "airline": f['airline']['name'] if f.get('airline') else 'Unknown',
                        "flight_number": f['flight']['iata'] if f.get('flight') else 'N/A',
                        "origin": f['departure']['airport'] if f.get('departure') else 'Unknown',
                        "arrival_time": datetime.strptime(f['arrival']['scheduled'], "%Y-%m-%dT%H:%M:%S+00:00").strftime("%H:%M") if f.get('arrival') and f['arrival'].get('scheduled') else "00:00"
                    }
                    real_flights.append(flight)
                except: continue
        if real_flights:
            set_cache("flights", real_flights)
            return real_flights
        return get_flight_data_demo()
    except: return get_flight_data_demo()

def analyze_flights():
    flights = get_flight_data_demo() if USE_DEMO_DATA else get_flight_data_real()
    if not flights: flights = get_flight_data_demo()
    smart_alerts = []
    for f in flights:
        origin = f['origin']
        arrival_time_str = f['arrival_time']
        profile = None
        for zone, data in FLIGHT_PROFILE.items():
            if any(hub in origin for hub in data['hubs']):
                profile = data
                matched_zone = zone
                break
        if profile:
            try:
                h, m = map(int, arrival_time_str.split(':'))
                total_mins = h * 60 + m + profile['exit_delay']
                exit_time_str = f"{(total_mins // 60) % 24:02}:{total_mins % 60:02}"
                fare_parts = profile['fare_range'].split('-')
                smart_alerts.append({
                    "airline": f['airline'], "flight": f['flight_number'], "origin": origin,
                    "land_time": arrival_time_str, "exit_time": exit_time_str,
                    "fare_range": profile['fare_range'], "fare_min": int(fare_parts[0]), "fare_max": int(fare_parts[1]),
                    "note": profile['comment'], "zone": matched_zone, "icon": profile['icon'], "color": profile['color']
                })
            except: pass
    smart_alerts.sort(key=lambda x: x['exit_time'])
    return smart_alerts, len(flights)

@app.route('/debug')
def debug_paths():
    files = []
    for root, dirs, filenames in os.walk(base_dir):
        for f in filenames:
            files.append(os.path.relpath(os.path.join(root, f), base_dir))
    return jsonify({
        "base_dir": base_dir,
        "files": files,
        "template_folder": app.template_folder,
        "static_folder": app.static_folder,
        "index_exists": os.path.exists(os.path.join(base_dir, 'index.html'))
    })

@app.route('/')
def index():
    return render_template('index.html', airport=AIRPORT_CODE)

@app.route('/api/flights')
def get_flights():
    alerts, total = analyze_flights()
    driver_lat = request.args.get('lat', type=float)
    driver_lng = request.args.get('lng', type=float)
    
    EVENT_LOCATIONS = [
        {"name": "Impact Arena", "event": "HEAVEN SKATEBOARD", "end_time": "22:00", "people": "20,000", "fare_range": "300-500", "fare_min": 300, "fare_max": 500, "icon": "🎸", "lat": 13.911, "lng": 100.550},
        {"name": "BITEC Bangna", "event": "Motor Show 2026", "end_time": "21:00", "people": "50,000", "fare_range": "200-400", "fare_min": 200, "fare_max": 400, "icon": "🚗", "lat": 13.669, "lng": 100.610},
        {"name": "Rajamangala Stadium", "event": "Coldplay World Tour", "end_time": "23:00", "people": "60,000", "fare_range": "400-800", "fare_min": 400, "fare_max": 800, "icon": "🏟️", "lat": 13.755, "lng": 100.622}
    ]
    
    city_alerts = []
    for event in EVENT_LOCATIONS:
        if driver_lat and driver_lng:
            import math
            R = 6371
            dlat, dlon = math.radians(event['lat'] - driver_lat), math.radians(event['lng'] - driver_lng)
            a = math.sin(dlat / 2)**2 + math.cos(math.radians(driver_lat)) * math.cos(math.radians(event['lat'])) * math.sin(dlon / 2)**2
            dist = R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            event['distance'], event['score'], event['note'] = f"{dist:.1f} km", ((event['fare_min'] + event['fare_max']) / 2) - (dist * 5), f"ห่าง {dist:.1f} กม."
        else:
            event['distance'], event['score'], event['note'] = None, 0, "ไม่ทราบพิกัด"
        city_alerts.append(event)

    if driver_lat: city_alerts.sort(key=lambda x: x['score'], reverse=True)
    return jsonify({
        "alerts": alerts, "city_alerts": city_alerts, "total_flights": total,
        "high_value_count": len(alerts) + len(city_alerts), "current_time": datetime.now().strftime("%H:%M"),
        "airport": AIRPORT_CODE
    })

@app.route('/api/traffic')
def get_traffic():
    return jsonify({"incidents": [], "count": 0, "source": "Longdo Traffic", "updated": datetime.now().strftime("%H:%M")})

@app.route('/api/news')
def get_news():
    return jsonify({"news": [], "count": 0, "updated": datetime.now().strftime("%H:%M")})

# EV stations and AI agent routes can be added here if needed, 
# but let's keep it simple to fix the deployment first.

if __name__ == '__main__':
    app.run(debug=True, port=5000)