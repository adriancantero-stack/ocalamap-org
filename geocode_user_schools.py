import json
import time
import urllib.request
import urllib.parse

def geocode(address):
    if "Ocala, FL" not in address:
        address += ", Ocala, FL"
        
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
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
        print(f"Error geocoding {address}: {e}")
    return None, None

def main():
    with open('user_schools_parsed.json', 'r') as f:
        schools = json.load(f)
    
    for school in schools:
        print(f"Geocoding {school['name']}...")
        if school['address'] == "Ocala, FL (mesma região)":
             # Fallback for generic address
             school['lat'] = 29.1872
             school['lng'] = -82.1401
             print("  Using default Ocala coordinates")
        else:
            lat, lng = geocode(school['address'])
            if lat and lng:
                school['lat'] = lat
                school['lng'] = lng
                print(f"  Found: {lat}, {lng}")
            else:
                print("  Not found")
        
        # Generate ID
        school['id'] = school['name'].lower().replace(' ', '-').replace('.', '').replace(',', '').replace("'", "").replace("’", "") + '-user'
        
        time.sleep(1.1) # Respect rate limits
        
    with open('user_schools_geocoded.json', 'w') as f:
        json.dump(schools, f, indent=2)

if __name__ == "__main__":
    main()
