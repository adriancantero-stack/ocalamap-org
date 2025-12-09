import json

def main():
    # Load the schools data
    with open('user_schools_geocoded_fixed.json', 'r') as f:
        schools = json.load(f)
    
    # List of schools that should be private based on user_schools_raw.txt
    # I'll check for "Tipo: Privada" in the raw text logic, but here I'll just list the IDs or names that need changing.
    # Since I don't want to re-parse everything, I'll iterate and check names against a list of known private schools from the text file.
    
    private_schools_names = [
        "Child’s Haven South", "Time Out Respite Center", "Just For Kids Academy", "Cherished Development Schools",
        "Reach Early Education Center", "Righteous Seed Child Care Center", "Hobby Horse Ed Childcare Center",
        "Tots-Tots Inc", "Small Talk II Child Care", "Jones Family Child Care", "Graceway Academy",
        "Country Learning Center", "Heavenly Hope Childcare Center", "C F Learning Lab School Center",
        "Howard Academy", "C S D Howard Academy Head Start", "Angels in Arms", "Academic Playland Child Care Center",
        "Highlands Baptist Day Care", "Future Stars Academy", "Kid’s Choice Academy", "Central Florida Child Care Center",
        "Newborn Family Day Care Home", "Heaven’s Gate Child Development Center", "Debra Poole Family Day Care Center",
        "Family Ties Child Care Center", "First Step Family Child Care", "Pebbles-the Rock Day Care Center",
        "New Zion Child Care Learning Center", "St Paulin Christian School", "C D S Fort McCoy Head Start",
        "Children’s Palace East & Academy", "Contemporary Christian Academy", "Montessori Preparatory School of Ocala",
        "Totsville Preschool", "Grace Episcopal Church Early Learning Center/VPK", "C D S Mildred Bryant High School Head Start",
        "Advocacy Resource Center", "Kendrick Child Development Center", "All Stars Child Care Center – Ocala",
        "Lafaye’s Precious Angels Child Care Center", "First United Methodist Preschool", "Tiny Tykes Child Care",
        "Trinity Pre-School & Academy", "Training Up a Child Day Care", "Pathways to Learning Daycare",
        "Lil' Sunshines Day Care & VPK", "Over the Rainbow Learning Center & Preschool", "Kids Kampus Ocala Hills",
        "Cds Bronson Ii Head Start", "Grace Christian Academy", "Promiseland Academy", "Discovery Christian Learning Center",
        "Victory Academy Learning Center", "New Beginnings Child Care Center", "Nana Infants & Children Lc",
        "Make A Joyful Noise Academy", "Loving Care Pre-School", "Little Treasures Learning Center",
        "Kiddieklub Early Learning Center", "First Steps Pre-School", "Discovery Christian Learning Center",
        "Creative Kids Pre-School", "Children’s Palace West Child Care Center", "Carousel Early Learning Center",
        "CDS Thelma A Griffith Child Care Center", "Building Blocks PA-Ocala", "Building Blocks PA-Ocala (segunda unidade)",
        "Achieve Learning Center", "Creative Clinic Child Care Center-for-Infants", "Kingdom Christian Academy/Precious Children Preschool",
        "Victory Academy Ocala", "Christian Academy Of Hope", "Grace Christian School", "The Cornerstone School",
        "New Generation School", "St John Lutheran School", "Montessori Preparatory School", "Happy Hearts Kindergarten",
        "Hale Academy", "Living Waters Christian Academy", "Cornerstone Academy – Ocala", "Family Ties Day Care Center",
        "Sweethearts Day Care"
    ]
    
    updated_count = 0
    
    for school in schools:
        if school['name'] in private_schools_names:
            school['category'] = "Schools - Private"
            updated_count += 1
            
    print(f"Updated {updated_count} schools to 'Schools - Private'")
    
    with open('user_schools_geocoded_fixed.json', 'w') as f:
        json.dump(schools, f, indent=2)

if __name__ == "__main__":
    main()
