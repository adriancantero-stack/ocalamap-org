import json

def main():
    with open('schools_data_geocoded.json', 'r') as f:
        schools = json.load(f)
    
    # Fix St. John Lutheran School
    for school in schools:
        if school['name'] == "St. John Lutheran School":
            school['lat'] = 29.1691436
            school['lng'] = -82.1259249
    
    # Print formatted objects
    for school in schools:
        print("  {")
        print(f'    "id": "{school["id"]}",')
        print(f'    "name": "{school["name"]}",')
        print(f'    "category": "{school["category"]}",')
        print(f'    "address": "{school["address"]}",')
        print(f'    "city": "{school["city"]}",')
        print(f'    "state": "{school["state"]}",')
        print(f'    "rating": "{school["rating"]}",')
        print(f'    "grades": "{school["grades"]}",')
        print(f'    "lat": {school["lat"]},')
        print(f'    "lng": {school["lng"]}')
        print("  },")

if __name__ == "__main__":
    main()
