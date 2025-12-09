import json
import time
import urllib.request
import urllib.parse

def geocode(address):
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
    with open('schools_data.json', 'r') as f:
        schools = json.load(f)
    
    for school in schools:
        print(f"Geocoding {school['name']}...")
        lat, lng = geocode(school['address'])
        if lat and lng:
            school['lat'] = lat
            school['lng'] = lng
            print(f"  Found: {lat}, {lng}")
        else:
            print("  Not found")
        
        # Generate ID
        school['id'] = school['name'].lower().replace(' ', '-').replace('.', '').replace(',', '') + '-school'
        
        time.sleep(1) # Respect rate limits
        
    with open('schools_data_geocoded.json', 'w') as f:
        json.dump(schools, f, indent=2)

if __name__ == "__main__":
    main()
