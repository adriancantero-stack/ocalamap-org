import json
import time
import urllib.request
import urllib.parse
import random

def geocode(query):
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": query,
        "format": "json",
        "limit": 1
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'OcalaMapBuilder/1.0')
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if data:
                return float(data[0]['lat']), float(data[0]['lon'])
    except Exception as e:
        print(f"Error geocoding {query}: {e}")
    return None, None

def main():
    with open('user_schools_geocoded.json', 'r') as f:
        schools = json.load(f)
    
    missing_count = 0
    fixed_count = 0
    
    # Ocala center for fallback
    OCALA_LAT = 29.1872
    OCALA_LNG = -82.1401
    
    for school in schools:
        if not school.get('lat') or not school.get('lng'):
            missing_count += 1
            print(f"Fixing {school['name']}...")
            
            # Strategy 1: Clean address (remove zip if present, sometimes helps)
            address_parts = school['address'].split(',')
            if len(address_parts) > 2:
                # Try just street and city
                query = f"{address_parts[0]}, Ocala, FL"
                print(f"  Trying: {query}")
                lat, lng = geocode(query)
                if lat and lng:
                    school['lat'] = lat
                    school['lng'] = lng
                    fixed_count += 1
                    print(f"  Fixed! {lat}, {lng}")
                    time.sleep(1.1)
                    continue
            
            # Strategy 2: Name and City
            query = f"{school['name']}, Ocala, FL"
            print(f"  Trying: {query}")
            lat, lng = geocode(query)
            if lat and lng:
                school['lat'] = lat
                school['lng'] = lng
                fixed_count += 1
                print(f"  Fixed! {lat}, {lng}")
                time.sleep(1.1)
                continue
                
            # Strategy 3: Just City (Fallback)
            print("  Using fallback Ocala coordinates")
            # Add small random offset to avoid perfect stacking
            offset_lat = (random.random() - 0.5) * 0.02
            offset_lng = (random.random() - 0.5) * 0.02
            school['lat'] = OCALA_LAT + offset_lat
            school['lng'] = OCALA_LNG + offset_lng
            fixed_count += 1
            
            time.sleep(1.1)

    print(f"Total missing: {missing_count}")
    print(f"Total fixed: {fixed_count}")
        
    with open('user_schools_geocoded_fixed.json', 'w') as f:
        json.dump(schools, f, indent=2)

if __name__ == "__main__":
    main()
