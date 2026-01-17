from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
import random
import requests
import os

app = Flask(__name__)

# ================= CONFIGURATION =================
LINE_NOTIFY_TOKEN = os.environ.get("LINE_NOTIFY_TOKEN", "YOUR_LINE_TOKEN_HERE")
AVIATION_STACK_API_KEY = os.environ.get("AVIATION_STACK_API_KEY", "003b542bbac8cb2c38d66e2cb0eb85d5")  # FREE: 100 calls/month!
NOSTRA_API_KEY = os.environ.get("NOSTRA_API_KEY", "YOUR_NOSTRA_KEY_HERE")  # Not working, use demo
FACEBOOK_ACCESS_TOKEN = os.environ.get("FACEBOOK_ACCESS_TOKEN", "EAAdJlLvWHb8BQV9KmMLu1FHYWRFw6LckdENOylZATD45HnYZCXZAuIHKJ38RFyQHoei56LQ7DrFofqn2JWuIqDUppqNmJL74zP1zZAW6fOdG8gfuTtZAZA3Ot7YJ4ZBg76RibrQebeKqkyHts8jFR89qgIUFZCTHZAG9bR5WOqZBhn5cwTt3XHj8HfGoFfvpgnkr4CCUHlJcOIluDD9wI0ZAuduFz6dsWcFOCErBuJPSZAEVGzwRhjLgY6yfaiw6EdrGO4FyNciG3ModnRDA0a2FUwxxRWQt0IDSl8OsVpkgSxSZAeRmk3SZCUCwZAicdnAGhgjrFO3SdYniX4jQPNz")
USE_DEMO_DATA = os.environ.get("USE_DEMO_DATA", "False").lower() == "true"  # Now using REAL API (with caching!)
AIRPORT_CODE = os.environ.get("AIRPORT_CODE", "BKK")
# =================================================

# ================= CACHING SYSTEM (SAVE API CALLS!) =================
# Cache stores API results to avoid repeated calls
CACHE = {
    "flights": {"data": None, "expires": None},
    "traffic": {"data": None, "expires": None},
    "news": {"data": None, "expires": None}
}
CACHE_DURATION_MINUTES = 10  # Cache for 10 minutes (saves API calls!)
API_CALL_COUNT = {"flights": 0, "traffic": 0, "news": 0}  # Track usage

def get_cached(key):
    """Get cached data if not expired"""
    if CACHE[key]["data"] and CACHE[key]["expires"]:
        if datetime.now() < CACHE[key]["expires"]:
            return CACHE[key]["data"]
    return None

def set_cache(key, data):
    """Store data in cache with expiration"""
    CACHE[key]["data"] = data
    CACHE[key]["expires"] = datetime.now() + timedelta(minutes=CACHE_DURATION_MINUTES)
    API_CALL_COUNT[key] += 1
    print(f"๐” API Call #{API_CALL_COUNT[key]} for {key} (cached for {CACHE_DURATION_MINUTES} mins)")
# ===================================================================

FLIGHT_PROFILE = {
    "Europe": {
        "hubs": ["London", "Frankfurt", "Paris", "Zurich", "Munich", "Amsterdam", "Helsinki", "Copenhagen"],
        "exit_delay": 50,
        "fare_range": "500-800",
        "comment": "เธเธฃเธฐเน€เธเนเธฒเน€เธขเธญเธฐ เน€เธเนเธฒเน€เธกเธทเธญเธเนเธเธฅ (เธชเธธเธเธธเธกเธงเธดเธ—/เธชเธตเธฅเธม)",
        "icon": "๐’ถ",
        "color": "#3B82F6"
    },
    "MiddleEast": {
        "hubs": ["Dubai", "Doha", "Abu Dhabi", "Istanbul", "Tel Aviv", "Riyadh", "Kuwait"],
        "exit_delay": 60,
        "fare_range": "450-650",
        "comment": "เธกเธฒเน€เธเนเธเธเธฃเธญเธเธเธฃเธฑเธงเนเธซเธญเน เธ—เธดเธเธซเธเธฑเธ (เนเธเธเธเธฒเธเธฒ)",
        "icon": "๐ข๏ธ",
        "color": "#F59E0B"
    },
    "Russia": {
        "hubs": ["Moscow", "Saint Petersburg", "Novosibirsk"],
        "exit_delay": 55,
        "fare_range": "500-1500",
        "comment": "เนเธญเธเธฒเธชเน€เธซเธกเธฒเนเธเธเธฑเธ—เธขเธฒ/เธซเธฑเธงเธซเธดเธเธชเธนเธเธกเธฒเธ",
        "icon": "๐ท๐บ",
        "color": "#EF4444"
    },
    "EastAsia": {
        "hubs": ["Tokyo", "Osaka", "Seoul", "Taipei"],
        "exit_delay": 45,
        "fare_range": "400-550",
        "comment": "เธชเธธเธ เธฒเธ เธเนเธฒเธขเธ•เธฃเธ (เนเธ•เนเธญเธฒเธเธเธฐเนเธเน App เน€เธฃเธตเธขเธเธฃเธ–)",
        "icon": "๐ฏ๐ต",
        "color": "#EC4899"
    },
    "China": {
        "hubs": ["Shanghai", "Beijing", "Guangzhou", "Chengdu", "Kunming"],
        "exit_delay": 75,
        "fare_range": "350-500",
        "comment": "เธฃเธฐเธงเธฑเธ! เธฃเธญเธเธฒเธเธ•เธฃเธงเธเธงเธตเธเนเธฒ (เนเธเนเธเธเธฃเธฑเธเธ”เธฒ)",
        "icon": "๐จ๐ณ",
        "color": "#F97316"
    },
    "India": {
        "hubs": ["Delhi", "Mumbai", "Kolkata", "Bangalore"],
        "exit_delay": 70,
        "fare_range": "350-500",
        "comment": "เนเธเนเธเธเธเธฃเธฐเธ•เธนเธเนเธณ/เธเธฒเธซเธธเธฃเธฑเธ”",
        "icon": "๐ฎ๐ณ",
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
    # Check cache first to save API calls!
    cached = get_cached("flights")
    if cached:
        print("โ… Using cached flight data (no API call)")
        return cached
    
    try:
        url = "http://api.aviationstack.com/v1/flights"
        params = {
            'access_key': AVIATION_STACK_API_KEY,
            'arr_iata': AIRPORT_CODE,
            'flight_status': 'active',
            'limit': 20  # Limit results to save bandwidth
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        # Check for API errors (e.g., quota exceeded)
        if 'error' in data:
            print(f"โ ๏ธ AviationStack Error: {data['error'].get('message', 'Unknown')}")
            return get_flight_data_demo()
        
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
                except Exception:
                    continue  # Skip malformed entries
        
        # Cache the results!
        if real_flights:
            set_cache("flights", real_flights)
            return real_flights
        else:
            return get_flight_data_demo()
            
    except Exception as e:
        print(f"โ ๏ธ API Error: {e} (Switching to Demo Data)")
        return get_flight_data_demo()

def analyze_flights():
    if USE_DEMO_DATA:
        flights = get_flight_data_demo()
    else:
        flights = get_flight_data_real()
        if not flights: # Fallback if real data is empty
            flights = get_flight_data_demo()
            
    smart_alerts = []
    
    for f in flights:
        origin = f['origin']
        arrival_time_str = f['arrival_time']
        
        matched_zone = None
        profile = None
        
        for zone, data in FLIGHT_PROFILE.items():
            if any(hub in origin for hub in data['hubs']):
                matched_zone = zone
                profile = data
                break
        
        if profile:
            try:
                h, m = map(int, arrival_time_str.split(':'))
                total_mins = h * 60 + m + profile['exit_delay']
                exit_h = (total_mins // 60) % 24
                exit_m = total_mins % 60
                exit_time_str = f"{exit_h:02}:{exit_m:02}"
                
                fare_parts = profile['fare_range'].split('-')
                fare_min = int(fare_parts[0])
                fare_max = int(fare_parts[1])
                
                smart_alerts.append({
                    "airline": f['airline'],
                    "flight": f['flight_number'],
                    "origin": origin,
                    "land_time": arrival_time_str,
                    "exit_time": exit_time_str,
                    "fare_range": profile['fare_range'],
                    "fare_min": fare_min,
                    "fare_max": fare_max,
                    "note": profile['comment'],
                    "zone": matched_zone,
                    "icon": profile['icon'],
                    "color": profile['color']
                })
            except:
                pass
    
    smart_alerts.sort(key=lambda x: x['exit_time'])
    return smart_alerts, len(flights)

@app.route('/')
def index():
    return render_template('index.html', airport=AIRPORT_CODE)

import math

def calculate_distance(lat1, lon1, lat2, lon2):
    # Haversine formula to calculate distance between two points
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@app.route('/api/flights')
def get_flights():
    alerts, total = analyze_flights()
    
    # Get Driver Location (if sent)
    driver_lat = request.args.get('lat', type=float)
    driver_lng = request.args.get('lng', type=float)
    
    # ================= NEW: City Event Radar =================
    EVENT_LOCATIONS = [
        {
            "name": "Impact Arena",
            "type": "Concert",
            "event": "HEAVEN SKATEBOARD",
            "end_time": "22:00",
            "people": "20,000",
            "fare_range": "300-500",
            "fare_min": 300,
            "fare_max": 500,
            "icon": "๐ธ",
            "lat": 13.911,
            "lng": 100.550
        },
        {
            "name": "BITEC Bangna",
            "type": "Exhibition",
            "event": "Motor Show 2026",
            "end_time": "21:00",
            "people": "50,000",
            "fare_range": "200-400",
            "fare_min": 200,
            "fare_max": 400,
            "icon": "๐—",
            "lat": 13.669,
            "lng": 100.610
        },
        {
            "name": "Rajamangala Stadium",
            "type": "Concert",
            "event": "Coldplay World Tour",
            "end_time": "23:00",
            "people": "60,000",
            "fare_range": "400-800",
            "fare_min": 400,
            "fare_max": 800,
            "icon": "๐๏ธ",
            "lat": 13.755,
            "lng": 100.622
        }
    ]
    
    city_alerts = []
    
    for event in EVENT_LOCATIONS:
        # Calculate Distance & Score if driver location exists
        if driver_lat and driver_lng:
            dist = calculate_distance(driver_lat, driver_lng, event['lat'], event['lng'])
            event['distance'] = f"{dist:.1f} km"
            # Smart Score: (Avg Fare) - (Distance * 5 Baht/km fuel estimation)
            avg_fare = (event['fare_min'] + event['fare_max']) / 2
            score = avg_fare - (dist * 5)
            event['score'] = score
            event['note'] = f"เธซเนเธฒเธ {dist:.1f} เธเธก."
        else:
            event['distance'] = None
            event['score'] = 0
            event['note'] = "เนเธกเนเธ—เธฃเธฒเธเธเธดเธเธฑเธ”"
            
        city_alerts.append(event)

    # Sort City Alerts by Score (if location provided) or by Time (default)
    if driver_lat:
        city_alerts.sort(key=lambda x: x['score'], reverse=True)

    now = datetime.now().strftime("%H:%M")
    return jsonify({
        "alerts": alerts,
        "city_alerts": city_alerts, 
        "total_flights": total,
        "high_value_count": len(alerts) + len(city_alerts),
        "current_time": now,
        "airport": AIRPORT_CODE,
        "driver_loc": {"lat": driver_lat, "lng": driver_lng} if driver_lat else None
    })

# ================= LONGDO TRAFFIC API =================
LONGDO_API_KEY = os.environ.get("LONGDO_API_KEY", "40e07fdaa6a0cc5137da6b8ce3ebf055")
USE_DEMO_TRAFFIC = os.environ.get("USE_DEMO_TRAFFIC", "False").lower() == "true"  # Now using REAL Longdo Traffic data!

def get_traffic_incidents_demo():
    """Mock traffic data for demo purposes"""
    return [
        {
            "type": "accident",
            "icon": "๐—๐’ฅ",
            "title": "เธญเธธเธเธฑเธ•เธดเน€เธซเธ•เธธเธฃเธ–เธเธเธเธฑเธ",
            "location": "เธ–เธเธเธเธฃเธฐเธฃเธฒเธก 2 เธเธฒเธญเธญเธ เธเธก.15",
            "lat": 13.627,
            "lng": 100.415,
            "time": "18:30",
            "severity": "high"
        },
        {
            "type": "construction",
            "icon": "๐ง",
            "title": "เธเนเธญเธกเธ–เธเธ",
            "location": "เธ—เธฒเธเธ”เนเธงเธเธจเธฃเธตเธฃเธฑเธ เธเธฒเน€เธเนเธฒ",
            "lat": 13.780,
            "lng": 100.540,
            "time": "06:00-22:00",
            "severity": "medium"
        },
        {
            "type": "flood",
            "icon": "๐",
            "title": "เธเนเธณเธ—เนเธงเธกเธเธฑเธ",
            "location": "เนเธขเธเธญเนเธจเธ เธ–เธเธเธชเธธเธเธธเธกเธงเธดเธ—",
            "lat": 13.737,
            "lng": 100.560,
            "time": "19:00",
            "severity": "medium"
        },
        {
            "type": "broken_vehicle",
            "icon": "๐โ ๏ธ",
            "title": "เธฃเธ–เน€เธชเธตเธขเธเธญเธ”เธเธงเธฒเธเธ—เธฒเธ",
            "location": "เธ—เธฒเธเธ”เนเธงเธเธเธนเธฃเธเธฒเธงเธดเธ—เธต เธเธก.8",
            "lat": 13.720,
            "lng": 100.620,
            "time": "19:15",
            "severity": "low"
        }
    ]

def get_traffic_incidents_real():
    """Fetch real traffic data from Longdo Events API"""
    try:
        # Query 1: Accidents
        url = "https://api.longdo.com/POIService/json/search"
        params_acc = {
            'key': LONGDO_API_KEY,
            'tag': 'accident',
            'limit': 10,
            'span': '24h'
        }
        res_acc = requests.get(url, params=params_acc, timeout=10).json()
        
        # Query 2: Construction
        params_con = {
            'key': LONGDO_API_KEY,
            'tag': 'construction',
            'limit': 5,
            'span': '1w'
        }
        res_con = requests.get(url, params=params_con, timeout=10).json()

        incidents = []
        
        # Process Accidents
        if 'data' in res_acc:
            for item in res_acc['data']:
                incidents.append({
                    "type": "accident",
                    "icon": "๐—๏ฟฝ",
                    "title": item.get('name', 'เธญเธธเธเธฑเธ•เธดเน€เธซเธ•เธธ'),
                    "location": item.get('address', 'เนเธกเนเธฃเธฐเธเธธ'),
                    "lat": item.get('lat', 0),
                    "lng": item.get('lon', 0),
                    "time": "Today",
                    "severity": "high"
                })

        # Process Construction
        if 'data' in res_con:
            for item in res_con['data']:
                incidents.append({
                    "type": "construction",
                    "icon": "๐ง",
                    "title": item.get('name', 'เธเธฒเธเธเนเธญเธชเธฃเนเธฒเธ'),
                    "location": item.get('address', 'เนเธกเนเธฃเธฐเธเธธ'),
                    "lat": item.get('lat', 0),
                    "lng": item.get('lon', 0),
                    "time": "Ongoing",
                    "severity": "medium"
                })

        return incidents if incidents else [{"type": "info", "icon": "โ…", "title": "No Incidents", "location": "Traffic Clear", "time": "Now", "severity": "low"}]
    except Exception as e:
        print(f"โ ๏ธ Longdo API Error: {e}")
        return [{"type": "error", "icon": "โ", "title": "API Error", "location": str(e), "time": "Now", "severity": "high"}]

@app.route('/api/traffic')
def get_traffic():
    if USE_DEMO_TRAFFIC:
        incidents = get_traffic_incidents_demo()
    else:
        incidents = get_traffic_incidents_real()
    
    return jsonify({
        "incidents": incidents,
        "count": len(incidents),
        "source": "Longdo Traffic / iTIC",
        "updated": datetime.now().strftime("%H:%M")
    })

# ================= FACEBOOK TRAFFIC NEWS API =================
# FACEBOOK_ACCESS_TOKEN already set above
USE_DEMO_NEWS = os.environ.get("USE_DEMO_NEWS", "False").lower() == "true"  # Now using REAL Facebook data!

# Reliable Thai Traffic Facebook Pages
TRAFFIC_PAGES = {
    "js100": {
        "page_id": "js100radio",
        "name": "เธเธช.100",
        "icon": "๐“ป"
    },
    "fm91": {
        "page_id": "fm91trafficpro",
        "name": "FM91 เธชเธงเธ.",
        "icon": "๐จ"
    },
    "highway": {
        "page_id": "HighwayPolice1193",
        "name": "เธ•เธณเธฃเธงเธเธ—เธฒเธเธซเธฅเธงเธงเธ",
        "icon": "๐”"
    }
}

def get_facebook_news_demo():
    """Mock Facebook news for demo purposes"""
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    current_hour = datetime.now().hour
    
    return [
        {
            "source": "เธเธช.100",
            "icon": "๐“ป",
            "message": f"๐—๐’ฅ เธญเธธเธเธฑเธ•เธดเน€เธซเธ•เธธเธฃเธ–เธเธเธเธฑเธ 3 เธเธฑเธ เธเธฃเธดเน€เธงเธเธ—เธฒเธเธ”เนเธงเธเธจเธฃเธตเธฃเธฑเธ เธเธฒเธญเธญเธ เธเธก.15 เธฃเธ–เธ•เธดเธ”เธซเธเธฑเธ เนเธเธฐเธเธณเนเธเนเน€เธชเนเธเธ—เธฒเธเธญเธทเนเธ",
            "time": f"{current_hour-1:02}:30",
            "date": today
        },
        {
            "source": "FM91 เธชเธงเธ.",
            "icon": "๐จ",
            "message": f"๐ง๏ธ เธเธเธ•เธเธซเธเธฑเธเธเธฃเธดเน€เธงเธเธ–เธเธเธงเธดเธ เธฒเธงเธ”เธต เธเธฒเน€เธเนเธฒ เธเนเธณเน€เธฃเธดเนเธกเธ—เนเธงเธกเธเธฑเธ เธเธฑเธเธเธตเนเธฃเธฐเธงเธฑเธ",
            "time": f"{current_hour:02}:15",
            "date": today
        },
        {
            "source": "เธ•เธณเธฃเธงเธเธ—เธฒเธเธซเธฅเธงเธงเธ",
            "icon": "๐”",
            "message": f"๐ง เธเธดเธ”เธเนเธญเธกเธ–เธเธ เธ–เธเธเธกเธดเธ•เธฃเธ เธฒเธ เธเธก.120 เน€เธเธดเธ”เนเธเนเน€เธฅเธเธเธงเธฒเนเธ”เนเน€เธฅเธเน€เธ”เธตเธขเธง",
            "time": f"{current_hour-2:02}:00",
            "date": today
        },
        {
            "source": "เธเธช.100",
            "icon": "๐“ป",
            "message": f"๐โ ๏ธ เธฃเธ–เธเธฃเธฃเธ—เธธเธเน€เธชเธตเธขเธเธญเธ”เธเธงเธฒเธเธ—เธฒเธ เธ–เธเธเธเธฃเธฐเธฃเธฒเธก 2 เธเธฒเธญเธญเธ เธเธก.32 เธเธนเนเธฃเธ–เธญเธขเธนเน",
            "time": f"{current_hour:02}:45",
            "date": today
        }
    ]

def get_facebook_news_real():
    """Fetch real posts from Facebook Graph API"""
    try:
        from datetime import datetime, timedelta
        
        all_posts = []
        today = datetime.now().strftime("%Y-%m-%d")
        
        for key, page in TRAFFIC_PAGES.items():
            url = f"https://graph.facebook.com/v18.0/{page['page_id']}/posts"
            params = {
                'access_token': FACEBOOK_ACCESS_TOKEN,
                'fields': 'message,created_time',
                'limit': 10
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if 'data' in data:
                for post in data['data']:
                    if 'message' in post:
                        # Parse date
                        created = post.get('created_time', '')[:10]
                        if created == today:  # Only today's posts
                            time_str = post.get('created_time', '')[11:16]
                            all_posts.append({
                                "source": page['name'],
                                "icon": page['icon'],
                                "message": post['message'][:200] + "..." if len(post['message']) > 200 else post['message'],
                                "time": time_str,
                                "date": created
                            })
        
        return all_posts if all_posts else get_facebook_news_demo()
    except Exception as e:
        print(f"โ ๏ธ Facebook API Error: {e}")
        return get_facebook_news_demo()

@app.route('/api/news')
def get_news():
    if USE_DEMO_NEWS:
        news = get_facebook_news_demo()
    else:
        news = get_facebook_news_real()
    
    # Sort by time (newest first)
    news.sort(key=lambda x: x['time'], reverse=True)
    
    return jsonify({
        "news": news,
        "count": len(news),
        "sources": list(TRAFFIC_PAGES.keys()),
        "updated": datetime.now().strftime("%H:%M")
    })

# ================= API USAGE MONITOR =================
@app.route('/api/usage')
def get_usage():
    """Monitor API usage to prevent unexpected charges"""
    return jsonify({
        "api_calls": API_CALL_COUNT,
        "cache_duration_mins": CACHE_DURATION_MINUTES,
        "aviationstack_limit":  "100 calls/month (FREE)",
        "current_month_usage": API_CALL_COUNT["flights"],
        "remaining_estimate": 100 - API_CALL_COUNT["flights"],
        "tip": "Cache is active! Each real API call is cached for 10 mins."
    })

# ================= EV CHARGING STATIONS =================
from ev_stations_data import EV_STATIONS_BANGKOK

@app.route('/api/ev-stations')
def get_ev_stations():
    driver_lat = request.args.get('lat', type=float)
    driver_lng = request.args.get('lng', type=float)
    
    stations = []
    for station in EV_STATIONS_BANGKOK:
        station_copy = station.copy()
        
        # Calculate distance if location provided
        if driver_lat and driver_lng:
            dist = calculate_distance(driver_lat, driver_lng, station['lat'], station['lng'])
            station_copy['distance'] = dist
            station_copy['distance_str'] = f"{dist:.1f} km"
        else:
            station_copy['distance'] = 999  # Default far distance
            station_copy['distance_str'] = "เนเธกเนเธ—เธฃเธฒเธเธฃเธฐเธขเธฐเธ—เธฒเธ"
        
        # Calculate price score (lower peak price = better)
        peak_price = float(station['pricing']['peak'].split()[0])
        station_copy['peak_price'] = peak_price
        
        stations.append(station_copy)
    
    # Sort by distance (nearest first)
    stations_by_distance = sorted(stations, key=lambda x: x['distance'])
    top_nearest = stations_by_distance[:3]
    
    # Sort by price (cheapest first)
    stations_by_price = sorted(stations, key=lambda x: x['peak_price'])
    top_cheapest = stations_by_price[:3]
    
    return jsonify({
        "top_nearest": top_nearest,
        "top_cheapest": top_cheapest,
        "all_stations": stations[:10],  # Show top 10 overall
        "count": len(stations),
        "updated": datetime.now().strftime("%H:%M"),
        "has_location": driver_lat is not None
    })

# ================= AI AGENT (DeepSeek via OpenRouter) =================
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "YOUR_OPENROUTER_KEY_HERE")
USE_AI_AGENT = os.environ.get("USE_AI_AGENT", "False").lower() == "true"

@app.route('/api/search-agent', methods=['POST'])
def search_agent():
    """AI-powered location search assistant"""
    if not USE_AI_AGENT:
        return jsonify({"advice": "เธเธตเน€เธเธญเธฃเนเธเธตเนเธ•เนเธญเธเธเธฒเธฃ OpenRouter API Key", "type": "error"})
    
    user_query = request.json.get('query', '')
    driver_lat = request.json.get('lat')
    driver_lng = request.json.get('lng')
    
    try:
        # Get current data
        alerts, _ = analyze_flights()
        
        # Build context
        context = f"""
        เธเธเธเธฑเธเนเธ—เนเธเธเธตเนเธญเธขเธนเนเธ—เธตเน: เธฅเธฐเธ•เธดเธเธนเธ” {driver_lat}, เธฅเธญเธเธเธดเธเธนเธ” {driver_lng}
        
        เน€เธ—เธตเนเธขเธงเธเธดเธเนเธเธฅเนเน€เธเธตเธขเธ:
        {[f"{a['flight']} เธเธฒเธ {a['origin']} เธญเธญเธเธกเธฒ {a['exit_time']}" for a in alerts[:3]]}
        
        เธเธณเธ–เธฒเธก: {user_query}
        
        เธ•เธญเธเธ เธฒเธฉเธฒเนเธ—เธข เธชเธฑเนเธเธเธฃเธฐเธเธฑเธ (เนเธกเนเน€เธเธดเธ 100 เธเธณ):
        """
        
        # Call DeepSeek via OpenRouter
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek/deepseek-r1-distill-qwen-32b",
                "messages": [{"role": "user", "content": context}]
            },
            timeout=15
        )
        
        data = response.json()
        advice = data['choices'][0]['message']['content']
        
        return jsonify({"advice": advice, "type": "success"})
    except Exception as e:
        return jsonify({"advice": f"เน€เธ เธดเธ”เธเนเธญเธเธดเธ”เธเธฅเธฒเธ”: {str(e)}", "type": "error"})

# Vercel will import this module, so we don't need the main block
# The app instance will be used directly
