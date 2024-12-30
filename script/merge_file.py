import os

# Get directory of current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get project root (parent directory of script)
project_path = os.path.dirname(script_dir)
# print(f'Project root: {project_path}')
filterGroupPath = project_path + "/filter_group/"

def merge_files_from_array(file_paths, output_file_name):
    output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../', output_file_name + '.filter')
    
    try:
        with open(output_file, 'w') as outfile:
            for file_path in file_paths:
                full_path = os.path.join(filterGroupPath, file_path)
                if os.path.exists(full_path):
                    with open(full_path, 'r') as infile:
                        content = infile.read()
                        outfile.write(content)
                        outfile.write('\n\n')  # Add separator between files
                else:
                    print(f"Warning: File not found - {full_path}")
        return True
    except Exception as e:
        print(f"Error merging files: {str(e)}")
        return False

if __name__ == "__main__":
    # Example usage
    test_files = [filterGroupPath+"show/rarity_magic.filter", filterGroupPath+"show/rarity_rare.filter"]
    merge_files_from_array(test_files, "test")
