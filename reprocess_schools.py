import json
import re

def parse_raw_data(filename):
    schools_info = {}
    current_section = None
    
    with open(filename, 'r') as f:
        lines = f.readlines()
        
    current_school = {}
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line == "Preschools / Daycares":
            current_section = "Schools - Preschool"
            continue
        elif line == "Elementary":
            current_section = "Schools - Elementary"
            continue
        elif line == "Middle": # Future proofing
            current_section = "Schools - Middle"
            continue
        elif line == "High": # Future proofing
            current_section = "Schools - High"
            continue
            
        # Check for school name (numbered list)
        name_match = re.match(r'^\d+\.\s+(.+)', line)
        if name_match:
            # Save previous school if exists
            if current_school:
                schools_info[current_school['name']] = current_school
            
            current_school = {
                'name': name_match.group(1).strip(),
                'section': current_section
            }
            continue
            
        # Check for Type
        type_match = re.search(r'\* Tipo: (.+)', line)
        if type_match:
            raw_type = type_match.group(1).strip()
            # Map types
            if "Privada" in raw_type:
                school_type = "Private"
            elif "Pública" in raw_type:
                school_type = "Public"
                if "Magnet" in raw_type:
                    school_type = "Public Magnet"
                elif "Charter" in raw_type:
                    school_type = "Public Charter"
                elif "District" in raw_type:
                    school_type = "Public District"
            else:
                school_type = raw_type # Fallback
            
            current_school['type'] = school_type
            
    # Save last school
    if current_school:
        schools_info[current_school['name']] = current_school
        
    return schools_info

def main():
    # 1. Parse raw data to get Types and Sections
    raw_info = parse_raw_data('user_schools_raw.txt')
    
    # 2. Load geocoded data
    with open('user_schools_geocoded_fixed.json', 'r') as f:
        geocoded_schools = json.load(f)
        
    # 3. Merge
    updated_schools = []
    
    for school in geocoded_schools:
        name = school['name']
        # Try exact match first
        info = raw_info.get(name)
        
        # If not found, try fuzzy match (sometimes encoding issues or minor diffs)
        if not info:
            for k, v in raw_info.items():
                if k in name or name in k:
                    info = v
                    break
        
        if info:
            school['category'] = info['section']
            school['type'] = info.get('type', '')
            # Ensure we don't have "Schools - Private" anymore
        else:
            # If not found in raw text (maybe manually added?), keep as is or default
            # But wait, all user schools came from raw text.
            print(f"Warning: Could not find info for {name}")
            
        updated_schools.append(school)
        
    # 4. Output formatted JS
    print("const places = [")
    
    # We need to include the existing static places from index.html if we want to replace the WHOLE array,
    # OR we just output the user schools part to inject.
    # The user wants to "retirar a categoria privadas", so I should probably regenerate the user schools block.
    # The static schools in index.html (at the top) also have categories. 
    # I should probably just output the user schools part for injection, 
    # BUT I also need to make sure I don't accidentally keep the "Schools - Private" category for them.
    
    # Let's just output the JSON for now, and I'll use the format script to generate the JS block.
    with open('user_schools_final.json', 'w') as f:
        json.dump(updated_schools, f, indent=2)
        
    print(f"Processed {len(updated_schools)} schools.")

if __name__ == "__main__":
    main()
