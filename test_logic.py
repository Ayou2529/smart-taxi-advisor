import math

# --- 1. MOCK DATA (Copy from app.py) ---
EVENT_LOCATIONS = [
    {
        "name": "Impact Arena",
        "fare_min": 300,
        "fare_max": 500,
        "lat": 13.911,
        "lng": 100.550
    },
    {
        "name": "BITEC Bangna",
        "fare_min": 200,
        "fare_max": 400,
        "lat": 13.669,
        "lng": 100.610
    },
    {
        "name": "Rajamangala Stadium",
        "fare_min": 400,
        "fare_max": 800,
        "lat": 13.755,
        "lng": 100.622
    }
]

# --- 2. LOGIC FUNCTIONS ---
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def get_recommendation(driver_name, driver_lat, driver_lng):
    print(f"\n🚙 Driver: {driver_name} (Lat: {driver_lat}, Lng: {driver_lng})")
    print("-" * 50)
    
    scored_events = []
    for event in EVENT_LOCATIONS:
        dist = calculate_distance(driver_lat, driver_lng, event['lat'], event['lng'])
        
        # Logic: Avg Fare - (Distance * 5 Baht fuel/depreciation)
        avg_fare = (event['fare_min'] + event['fare_max']) / 2
        fuel_cost = dist * 5
        score = avg_fare - fuel_cost
        
        scored_events.append({
            "name": event['name'],
            "distance": dist,
            "avg_fare": avg_fare,
            "fuel_cost": fuel_cost,
            "score": score
        })
    
    # Sort by Score (Highest first)
    scored_events.sort(key=lambda x: x['score'], reverse=True)
    
    for i, res in enumerate(scored_events, 1):
        print(f"{i}. {res['name']}")
        print(f"   📏 Dist: {res['distance']:.1f} km | ⛽ Cost: {res['fuel_cost']:.0f}฿ | 💰 Fare: {res['avg_fare']:.0f}฿")
        print(f"   ⭐ Score: {res['score']:.1f} (Profit Potential)")

# --- 3. SCENARIOS ---

# Scenario A: Rama 2 (Central Rama 2 approx)
get_recommendation("Driver @ Rama 2", 13.627, 100.415)

# Scenario B: Lat Krabang (Suvarnabhumi approx area)
get_recommendation("Driver @ Lat Krabang", 13.723, 100.778)

# Scenario C: Rangsit (Near Impact)
get_recommendation("Driver @ Rangsit", 13.98, 100.61)
