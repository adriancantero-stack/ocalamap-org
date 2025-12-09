import json
import time
import requests
import random

def geocode_address(address):
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
        "limit": 1,
        "email": "antigravity@google.com" 
    }
    headers = {
        "User-Agent": "AntigravityAgent/1.0"
    }
    
    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
        else:
            return None
    except Exception as e:
        print(f"Error geocoding {address}: {e}")
        return None

def main():
    with open('user_schools_high_parsed.json', 'r') as f:
        schools = json.load(f)
        
    geocoded_schools = []
    
    # Ocala center for fallback
    OCALA_LAT = 29.1872
    OCALA_LNG = -82.1401
    
    for i, school in enumerate(schools):
        print(f"Processing {i+1}/{len(schools)}: {school['name']}")
        
        lat, lng = None, None
        
        # Strategy 1: Full address
        if school.get('address'):
            res = geocode_address(school['address'])
            if res:
                lat, lng = res
                print(f"  Found: {lat}, {lng}")
            else:
                # Strategy 2: Name + City
                query = f"{school['name']}, Ocala, FL"
                print(f"  Retrying with: {query}")
                time.sleep(1.1)
                res = geocode_address(query)
                if res:
                    lat, lng = res
                    print(f"  Found: {lat}, {lng}")
                else:
                    # Strategy 3: Fallback
                    print("  Failed. Using fallback.")
                    lat = OCALA_LAT + random.uniform(-0.02, 0.02)
                    lng = OCALA_LNG + random.uniform(-0.02, 0.02)
        
        school['lat'] = lat
        school['lng'] = lng
        
        # Generate ID
        school['id'] = school['name'].lower().replace(' ', '-').replace("'", "").replace("’", "") + "-high"
        
        geocoded_schools.append(school)
        time.sleep(1.1) # Rate limit
        
    with open('user_schools_high_geocoded.json', 'w') as f:
        json.dump(geocoded_schools, f, indent=2)
        
    print("Geocoding complete.")

if __name__ == "__main__":
    main()
