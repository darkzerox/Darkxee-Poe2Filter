import os
from urllib import request
import zipfile
import platform
import json
import shutil

# ค่าเริ่มต้น
owner = 'darkzerox'
repo = 'Darkxee-Poe2Filter'

def get_game_path():
    if platform.system() == 'Windows':
        return os.path.expandvars(r'%userprofile%\Documents\My Games\Path of Exile 2')
    else:  # Linux/MacOS
        home = os.path.expanduser('~')
        return os.path.join(home, 'steamapps/compatdata/2694490/pfx/drive_c/users/steamuser/My Documents/My Games/Path of Exile 2')

def fetch_url(url):
    try:
        with request.urlopen(url) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching URL: {str(e)}")
        return None

def get_latest_release(owner, repo):
    url = f'https://api.github.com/repos/{owner}/{repo}/releases/latest'
    response = fetch_url(url)
    if response:
        return json.loads(response)
    else:
        return None

def download_file(url, file_path):
    try:
        with request.urlopen(url) as response:
            with open(file_path, 'wb') as file:
                file.write(response.read())
        print(f"Successfully downloaded to {file_path}")
    except Exception as e:
        print(f"Error downloading file: {str(e)}")
        return False
    return True

def extract_file(file_path, extract_to):
    # Create a temporary extraction directory
    temp_dir = os.path.join(os.path.dirname(file_path), 'temp_extract')
    try:
        # Extract to temp directory first
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Find the extracted folder (usually repo-version)
        extracted_items = os.listdir(temp_dir)
        if len(extracted_items) == 1 and os.path.isdir(os.path.join(temp_dir, extracted_items[0])):
            source_dir = os.path.join(temp_dir, extracted_items[0])
            
            # Get the list of all items in the source directory
            items = os.listdir(source_dir)
            
            # Move each item to the final destination
            for item in items:
                source_item = os.path.join(source_dir, item)
                dest_item = os.path.join(extract_to, item)
                
                # Remove existing item if it exists
                if os.path.exists(dest_item):
                    if os.path.isdir(dest_item):
                        shutil.rmtree(dest_item)
                    else:
                        os.remove(dest_item)
                
                # Move the item
                if os.path.isdir(source_item):
                    shutil.copytree(source_item, dest_item)
                else:
                    shutil.copy2(source_item, dest_item)
                    
        print(f'Extracted files to {extract_to}')
    except Exception as e:
        print(f"Error during extraction: {str(e)}")
        raise
    finally:
        # Clean up temp directory
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

def update_if_needed():
    latest_release = get_latest_release(owner, repo)
    if not latest_release:
        print("Failed to fetch latest release information")
        return

    latest_version = latest_release['tag_name']
    print(f"Latest version found: {latest_version}")
    
    # Check if assets exist
    if 'assets' not in latest_release or not latest_release['assets']:
        print("No assets found in the release")
        # Fallback to downloading zip from source
        download_url = f"https://github.com/{owner}/{repo}/archive/refs/tags/{latest_version}.zip"
        asset_name = f"{repo}-{latest_version}.zip"
    else:
        asset = latest_release['assets'][0]
        download_url = asset['browser_download_url']
        asset_name = asset['name']
    
    print(f"Download URL: {download_url}")
    
    # Get game installation path
    game_path = get_game_path()
    version_file = os.path.join(game_path, 'dzx_filter_version.txt')
    
    # Read current version from game path
    if os.path.exists(version_file):
        with open(version_file, 'r') as f:
            current_version = f.read().strip()
    else:
        current_version = None

    print(f"Current version: {current_version}")
    print(f"Checking version file at: {version_file}")

    if current_version != latest_version:
        print(f'Updating from version {current_version} to {latest_version}')
        
        # Download the file
        if not download_file(download_url, asset_name):
            print("Failed to download update")
            return

        # Create game directory if it doesn't exist
        os.makedirs(game_path, exist_ok=True)

        try:
            extract_file(asset_name, game_path)
            # Update version file in game path
            with open(version_file, 'w') as f:
                f.write(latest_version)
            print(f'Successfully updated to {latest_version}')
        except Exception as e:
            print(f"Error during extraction: {str(e)}")
        finally:
            # Cleanup downloaded zip
            if os.path.exists(asset_name):
                os.remove(asset_name)
    else:
        print('Already up-to-date with version', current_version)

if __name__ == "__main__":
    update_if_needed()