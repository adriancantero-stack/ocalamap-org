import json
import re

# Read places data
with open('places.json', 'r') as f:
    places_data = f.read()

# Read index.html
with open('index.html', 'r') as f:
    html_content = f.read()

new_places_block = f"const places = {places_data};"

# Regex to replace `const places = [...];`
pattern = r"const places = \[[\s\S]*?\];"

# Use a lambda to avoid backslash escaping issues in the replacement string
new_html_content = re.sub(pattern, lambda m: new_places_block, html_content)

with open('index.html', 'w') as f:
    f.write(new_html_content)

print("Successfully injected places data into index.html")
