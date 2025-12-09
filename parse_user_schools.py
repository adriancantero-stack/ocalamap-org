import re
import json

def parse_schools(filename):
    with open(filename, 'r') as f:
        content = f.read()

    # Split by double newlines or section headers
    sections = content.split('\n\n')
    
    schools = []
    current_category = "Schools - Preschool" # Default
    
    for section in sections:
        section = section.strip()
        if not section:
            continue
            
        if "Preschools / Daycares" in section:
            current_category = "Schools - Preschool"
            continue
        if "Elementary" in section and len(section) < 20: # Header check
            current_category = "Schools - Elementary"
            continue
            
        # Parse individual school block
        # Format:
        # 1. Name
        # * Tipo: ...
        # * Endereço: ...
        # * Nota: ...
        # * Séries: ...
        
        lines = section.split('\n')
        if len(lines) < 2:
            continue
            
        # Extract Name (remove number prefix)
        name_line = lines[0]
        name_match = re.match(r'\d+\.\s+(.*)', name_line)
        if name_match:
            name = name_match.group(1).strip()
        else:
            name = name_line.strip()
            
        school = {
            "name": name,
            "category": current_category,
            "rating": "",
            "grades": "",
            "address": "",
            "city": "Ocala",
            "state": "FL"
        }
        
        for line in lines[1:]:
            if "* Tipo:" in line:
                tipo = line.split(":")[1].strip()
                # Map types if needed, but for now we rely on the section header
                # If it's explicitly "Elementar" in the Preschool section (unlikely) or vice versa
                if "Elementar" in tipo:
                    school["category"] = "Schools - Elementary"
                elif "Privada" in tipo:
                    # Keep as is (Preschool or Elementary) but maybe add a tag?
                    # For now, just use the section category
                    pass
            elif "* Endereço:" in line:
                school["address"] = line.split(":")[1].strip()
            elif "* Nota:" in line:
                rating = line.split(":")[1].strip()
                if rating and rating != "—" and rating != "★ —":
                    school["rating"] = rating.replace("★", "").strip()
            elif "* Séries:" in line:
                grades = line.split(":")[1].strip()
                if grades:
                    school["grades"] = grades
        
        schools.append(school)
        
    return schools

schools = parse_schools('user_schools_raw.txt')
print(json.dumps(schools, indent=2))
with open('user_schools_parsed.json', 'w') as f:
    json.dump(schools, f, indent=2)
