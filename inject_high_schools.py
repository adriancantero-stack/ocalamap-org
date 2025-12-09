import json

def main():
    with open('user_schools_high_geocoded.json', 'r') as f:
        new_schools = json.load(f)
    
    new_schools = [s for s in new_schools if s.get('lat') and s.get('lng')]
    
    with open('index.html', 'r') as f:
        lines = f.readlines()
        
    insert_index = -1
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].strip() == "];" or lines[i].strip() == "]":
            insert_index = i
            break
            
    if insert_index != -1:
        if not lines[insert_index-1].strip().endswith(','):
             lines[insert_index-1] = lines[insert_index-1].rstrip() + ",\n"
             
        new_lines = []
        for i, school in enumerate(new_schools):
            categories = school.get('categories', [])
            if not categories:
                categories = ["Schools - High"] 
            
            for cat in categories:
                cat_suffix = cat.split('-')[-1].strip().lower()
                unique_id = f"{school['id']}-{cat_suffix}"
                
                js_obj = "  {\n"
                js_obj += f'    "id": "{unique_id}",\n'
                js_obj += f'    "name": "{school["name"]}",\n'
                js_obj += f'    "category": "{cat}",\n'
                if school.get("type"):
                    js_obj += f'    "type": "{school["type"]}",\n'
                js_obj += f'    "address": "{school["address"]}",\n'
                js_obj += f'    "city": "Ocala",\n' 
                js_obj += f'    "state": "FL",\n'
                if school.get("rating"):
                    js_obj += f'    "rating": "{school["rating"]}",\n'
                if school.get("grades"):
                    js_obj += f'    "grades": "{school["grades"]}",\n'
                js_obj += f'    "lat": {school["lat"]},\n'
                js_obj += f'    "lng": {school["lng"]}\n'
                js_obj += "  },\n"
                new_lines.append(js_obj)

        lines[insert_index:insert_index] = new_lines
        
        with open('index.html', 'w') as f:
            f.writelines(lines)
            
        print(f"Injected {len(new_lines)} entries.")
    else:
        print("Could not find insertion point.")

if __name__ == "__main__":
    main()
