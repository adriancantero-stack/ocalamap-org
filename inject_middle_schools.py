import json

def main():
    # Load the new geocoded schools
    with open('user_schools_middle_geocoded.json', 'r') as f:
        new_schools = json.load(f)
    
    # Filter valid
    new_schools = [s for s in new_schools if s.get('lat') and s.get('lng')]
    
    # Read index.html
    with open('index.html', 'r') as f:
        lines = f.readlines()
        
    # Find the end of the places array
    # We want to insert BEFORE the closing bracket of the places array.
    # The places array ends with "];" or just "]".
    # In the previous injection, we replaced the user block.
    # Now we want to APPEND to it.
    # Actually, the previous injection replaced the block:
    #   // User provided schools
    #   ...
    #   ]
    
    # So we can find the closing bracket "  ]" or "];" at the end of the places definition.
    # Let's look for the last closing bracket before "const map =" or similar.
    
    insert_index = -1
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].strip() == "];" or lines[i].strip() == "]":
            insert_index = i
            break
            
    if insert_index != -1:
        # We need to add a comma to the previous item if it doesn't have one
        # But wait, the previous item might be on the line before insert_index.
        # Let's check line insert_index - 1.
        if not lines[insert_index-1].strip().endswith(','):
             lines[insert_index-1] = lines[insert_index-1].rstrip() + ",\n"
             
        # Generate JS strings
        new_lines = []
        for i, school in enumerate(new_schools):
            comma = "," if i < len(new_schools) - 1 else ""
            # We need to handle multiple categories if present?
            # The app only supports one category per object in the filter logic currently:
            # place.category === selectedCategory
            # If a school has multiple categories, we need multiple entries with different IDs.
            
            categories = school.get('categories', [])
            if not categories:
                # Fallback if logic failed
                categories = ["Schools - Middle"] 
            
            for cat in categories:
                # Create a unique ID for this category entry
                cat_suffix = cat.split('-')[-1].strip().lower()
                unique_id = f"{school['id']}-{cat_suffix}"
                
                # Check if this ID already exists in the file? 
                # A simple check might be good to avoid duplicates if we run this multiple times.
                # But for now, let's just append.
                
                js_obj = "  {\n"
                js_obj += f'    "id": "{unique_id}",\n'
                js_obj += f'    "name": "{school["name"]}",\n'
                js_obj += f'    "category": "{cat}",\n'
                if school.get("type"):
                    js_obj += f'    "type": "{school["type"]}",\n'
                js_obj += f'    "address": "{school["address"]}",\n'
                # City/State might be missing in parsed data, use defaults or extracted
                js_obj += f'    "city": "Ocala",\n' 
                js_obj += f'    "state": "FL",\n'
                if school.get("rating"):
                    js_obj += f'    "rating": "{school["rating"]}",\n'
                if school.get("grades"):
                    js_obj += f'    "grades": "{school["grades"]}",\n'
                js_obj += f'    "lat": {school["lat"]},\n'
                js_obj += f'    "lng": {school["lng"]}\n'
                js_obj += "  }"
                
                # Add comma if it's not the very last item of the very last school
                # But we are inserting a block.
                # All items in our block need commas, except maybe the last one IF we are at the end of the array.
                # Since we are inserting before "]", the last item of our block should NOT have a comma IF "]" is the end.
                # BUT, usually in JS array, trailing comma is fine.
                # However, to be safe, let's add comma to all, and rely on the fact that we are appending.
                # Wait, if we append, the previous last item (which we modified to have a comma) connects to our first item.
                # Our last item will be followed by "]" so it doesn't strictly need a comma, but it's allowed.
                
                js_obj += ",\n"
                new_lines.append(js_obj)

        # Remove comma from the very last inserted line if we want to be strict, 
        # but modern JS allows trailing commas.
        # Let's just insert.
        
        lines[insert_index:insert_index] = new_lines
        
        with open('index.html', 'w') as f:
            f.writelines(lines)
            
        print(f"Injected {len(new_lines)} entries.")
    else:
        print("Could not find insertion point.")

if __name__ == "__main__":
    main()
