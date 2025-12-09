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
    hospitals = [
        {
            "name": "AdventHealth Ocala",
            "address": "1500 SW 1st Ave, Ocala, FL 34471",
            "phone": "(352) 351-7200",
            "website": "https://www.adventhealth.com/hospital/adventhealth-ocala"
        },
        {
            "name": "HCA Florida Ocala Hospital",
            "address": "1431 SW 1st Ave, Ocala, FL 34471",
            "phone": "(352) 401-1000",
            "website": "https://www.hcafloridahealthcare.com/locations/ocala-hospital"
        },
        {
            "name": "HCA Florida West Marion Hospital",
            "address": "4600 SW 46th Ct, Ocala, FL 34474",
            "phone": "(352) 291-3000",
            "website": "https://www.hcafloridahealthcare.com/locations/west-marion-hospital"
        },
        {
            "name": "Kindred Hospital Ocala",
            "address": "1500 SW 1st Ave #5, Ocala, FL 34471",
            "phone": "(352) 671-3130",
            "website": "https://www.kindredhospitals.com/"
        },
        {
            "name": "The Vines Hospital",
            "address": "3130 SW 27th Ave, Ocala, FL 34471",
            "phone": "(352) 671-3130",
            "website": "https://thevineshospital.com"
        }
    ]
    
    geocoded_hospitals = []
    
    for hospital in hospitals:
        print(f"Geocoding {hospital['name']}...")
        lat, lng = geocode(hospital['address'])
        if lat and lng:
            hospital['lat'] = lat
            hospital['lng'] = lng
            print(f"  Found: {lat}, {lng}")
        else:
            print("  Not found")
            # Fallback or manual entry if needed, but for now let's hope it works
            
        hospital['id'] = hospital['name'].lower().replace(' ', '-').replace('.', '').replace(',', '')
        hospital['category'] = "Hospitals"
        hospital['city'] = "Ocala"
        hospital['state'] = "FL"
        
        geocoded_hospitals.append(hospital)
        time.sleep(1) 
        
    with open('hospitals_geocoded.json', 'w') as f:
        json.dump(geocoded_hospitals, f, indent=2)

if __name__ == "__main__":
    main()
