import json

def main():
    with open('user_schools_final.json', 'r') as f:
        schools = json.load(f)
    
    # Filter out schools without coordinates
    schools = [s for s in schools if s.get('lat') and s.get('lng')]
    
    # Print formatted objects
    print("  // User provided schools")
    for i, school in enumerate(schools):
        comma = "," if i < len(schools) - 1 else ""
        print("  {")
        print(f'    "id": "{school["id"]}",')
        print(f'    "name": "{school["name"]}",')
        print(f'    "category": "{school["category"]}",')
        if school.get("type"):
            print(f'    "type": "{school["type"]}",')
        print(f'    "address": "{school["address"]}",')
        print(f'    "city": "{school["city"]}",')
        print(f'    "state": "{school["state"]}",')
        if school.get("rating"):
            print(f'    "rating": "{school["rating"]}",')
        if school.get("grades"):
            print(f'    "grades": "{school["grades"]}",')
        print(f'    "lat": {school["lat"]},')
        print(f'    "lng": {school["lng"]}')
        print(f"  }}{comma}")

if __name__ == "__main__":
    main()
