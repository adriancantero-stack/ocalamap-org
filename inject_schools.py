import os

def main():
    # Read the new schools data
    with open('schools_to_inject.txt', 'r') as f:
        new_schools_content = f.read()
    
    # Read the index.html
    with open('index.html', 'r') as f:
        lines = f.readlines()
    
    # Find the start and end of the block to replace
    start_index = -1
    end_index = -1
    
    for i, line in enumerate(lines):
        if "// User provided schools" in line:
            start_index = i
        if start_index != -1 and line.strip() == "]":
            end_index = i
            break
            
    if start_index != -1 and end_index != -1:
        print(f"Replacing lines {start_index+1} to {end_index}")
        
        # Remove the trailing comma from the new content if it exists
        new_schools_content = new_schools_content.rstrip()
        if new_schools_content.endswith(','):
             new_schools_content = new_schools_content[:-1]
        
        # Construct the new content
        # We keep the lines before start_index
        # We insert the new content
        # We keep the lines from end_index (which is the closing bracket)
        
        new_lines = lines[:start_index]
        new_lines.append(new_schools_content + "\n")
        new_lines.extend(lines[end_index:])
        
        with open('index.html', 'w') as f:
            f.writelines(new_lines)
        print("Injection successful.")
    else:
        print("Could not find the block to replace.")

if __name__ == "__main__":
    main()
