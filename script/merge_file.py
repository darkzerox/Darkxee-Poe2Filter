import os

# Get directory of current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get project root (parent directory of script)
project_path = os.path.dirname(script_dir)
# Path to filter_group directory using os.path.join
filter_group_path = os.path.join(project_path,"dzx_filter","filter_group")

def merge_files_from_array(file_paths, output_file_name , removeSoundEffect = False):
    # Create output path using os.path.join
    output_file = os.path.join(project_path, f"{output_file_name}.filter")
    
    try:
        with open(output_file, 'w') as outfile:
            for file_path in file_paths:
                # Ensure file_path doesn't start with path separator
                file_path = file_path.lstrip(os.sep)
                # Create full path using os.path.join
                full_path = os.path.join(filter_group_path, file_path)
                
                if os.path.exists(full_path):
                    with open(full_path, 'r') as infile:
                        content = infile.read()
                        if removeSoundEffect:
                            content = '\n'.join(line for line in content.split('\n') 
                                              if 'CustomAlertSound' not in line)
                        outfile.write(content)
                        outfile.write('\n\n')  # Add separator between files
                else:
                    print(f"Warning: File not found - {full_path}")
        return True
    except Exception as e:
        print(f"Error merging files: {str(e)}")
        return False

if __name__ == "__main__":
    test_files = [
        "rarity_magic.filter",
        "rarity_rare.filter"
    ]
    
    test_file_path = os.path.join(project_path, "test.filter")
    if os.path.exists(test_file_path):
        try:
            os.remove(test_file_path)
        except Exception as e:
            print(f"Error removing file: {str(e)}")
            
    merge_files_from_array(test_files, "test")
