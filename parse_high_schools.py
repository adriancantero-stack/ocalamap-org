import json
import re

def parse_raw_data(filename):
    schools = []
    current_school = {}
    
    with open(filename, 'r') as f:
        lines = f.readlines()
        
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check for school name (numbered list)
        name_match = re.match(r'^\d+\.\s+(.+)', line)
        if name_match:
            if current_school:
                schools.append(current_school)
            
            current_school = {
                'name': name_match.group(1).strip(),
                'original_text': line
            }
            continue
            
        # Check for Type
        type_match = re.search(r'\* Tipo: (.+)', line)
        if type_match:
            raw_type = type_match.group(1).strip()
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
                school_type = raw_type
            current_school['type'] = school_type
            continue

        # Check for Address
        addr_match = re.search(r'\* Endereço: (.+)', line)
        if addr_match:
            current_school['address'] = addr_match.group(1).strip()
            continue

        # Check for Rating
        rating_match = re.search(r'\* Nota: (.+)', line)
        if rating_match:
            rating = rating_match.group(1).strip().replace('★', '').strip()
            if rating == "—" or "não classificada" in rating:
                rating = ""
            current_school['rating'] = rating
            continue

        # Check for Grades
        grades_match = re.search(r'\* Séries: (.+)', line)
        if grades_match:
            grades = grades_match.group(1).strip()
            current_school['grades'] = grades
            
            categories = []
            g_str = grades.lower()
            
            if 'pk' in g_str:
                categories.append("Schools - Preschool")
            
            if re.search(r'(^|[\s,])(k|1|2|3|4|5)([\s,–-]|$)', g_str):
                 categories.append("Schools - Elementary")
            elif re.search(r'(^|[\s,])(k|1|2|3|4|5)[–-]', g_str): 
                 categories.append("Schools - Elementary")
            
            if re.search(r'(^|[\s,])(6|7|8)([\s,–-]|$)', g_str):
                categories.append("Schools - Middle")
            elif re.search(r'[–-](6|7|8)', g_str): 
                categories.append("Schools - Middle")
            elif re.search(r'(6|7|8)[–-]', g_str): 
                categories.append("Schools - Middle")

            if re.search(r'(^|[\s,])(9|10|11|12)([\s,–-]|$)', g_str):
                categories.append("Schools - High")
            elif re.search(r'[–-](9|10|11|12)', g_str): 
                categories.append("Schools - High")
            
            if '12' in g_str and ('k' in g_str or 'pk' in g_str or '1' in g_str):
                if "Schools - Elementary" not in categories: categories.append("Schools - Elementary")
                if "Schools - Middle" not in categories: categories.append("Schools - Middle")
                if "Schools - High" not in categories: categories.append("Schools - High")
            
            if '6' in g_str and '12' in g_str:
                 if "Schools - Middle" not in categories: categories.append("Schools - Middle")
                 if "Schools - High" not in categories: categories.append("Schools - High")

            current_school['categories'] = list(set(categories)) 
            continue

    if current_school:
        schools.append(current_school)
        
    with open('user_schools_high_parsed.json', 'w') as f:
        json.dump(schools, f, indent=2)
        
    print(f"Parsed {len(schools)} schools.")

if __name__ == "__main__":
    parse_raw_data('user_schools_high_raw.txt')
