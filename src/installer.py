#!/usr/bin/env python3
"""
POE2 Filter Installer
ติดตั้งและอัพเดท filter สำหรับ Path of Exile 2
"""

import os
import sys
import shutil
import logging
import json
from pathlib import Path
from typing import Optional, Dict, List
from github_updater import GitHubUpdater
from filter_manager import FilterManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('installer.log'),
        logging.StreamHandler()
    ]
)

class POE2FilterInstaller:
    """Main installer class for POE2 filters"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config = self.load_config()
        self.github_updater = GitHubUpdater()
        self.filter_manager = FilterManager()
        
        # POE2 installation paths
        self.poe2_paths = [
            os.path.expanduser("~/Documents/My Games/Path of Exile 2"),
            os.path.expanduser("~/Documents/My Games/Path of Exile 2/User/"),
            os.path.expanduser("~/Documents/My Games/Path of Exile 2/User/Filters/")
        ]
        
    def load_config(self) -> Dict:
        """Load configuration from config file"""
        config_path = Path("config/settings.json")
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Error loading config: {e}")
        
        # Default config
        return {
            "github_repo": "your-username/dzx-filter-poe2",
            "current_version": "1.0.0",
            "auto_update": True,
            "backup_enabled": True
        }
    
    def find_poe2_directory(self) -> Optional[str]:
        """Find POE2 installation directory"""
        for path in self.poe2_paths:
            if os.path.exists(path):
                self.logger.info(f"Found POE2 directory: {path}")
                return path
        
        # Try to create directory if it doesn't exist
        default_path = self.poe2_paths[0]
        try:
            os.makedirs(default_path, exist_ok=True)
            self.logger.info(f"Created POE2 directory: {default_path}")
            return default_path
        except Exception as e:
            self.logger.error(f"Error creating POE2 directory: {e}")
            return None
    
    def check_for_updates(self) -> bool:
        """Check if there are updates available"""
        try:
            latest_version = self.github_updater.get_latest_version()
            current_version = self.config["current_version"]
            
            if self.github_updater.is_newer_version(latest_version, current_version):
                self.logger.info(f"Update available: {current_version} -> {latest_version}")
                return True
            else:
                self.logger.info("No updates available")
                return False
                
        except Exception as e:
            self.logger.error(f"Error checking for updates: {e}")
            return False
    
    def install_filters(self, poe2_path: str) -> bool:
        """Install filters to POE2 directory"""
        try:
            # Create filters directory
            filters_dir = os.path.join(poe2_path, "User", "Filters")
            os.makedirs(filters_dir, exist_ok=True)
            
            # Copy only essential filter files
            filter_files = [
                "dzx-poe2.filter",  # Main filter
            ]
            
            # Add dzx-poe2-*.filter files
            import glob
            additional_filters = glob.glob("dzx-poe2-*.filter")
            filter_files.extend(additional_filters)
            
            for filter_file in filter_files:
                if os.path.exists(filter_file):
                    dest_path = os.path.join(filters_dir, filter_file)
                    shutil.copy2(filter_file, dest_path)
                    self.logger.info(f"Installed: {filter_file}")
                else:
                    self.logger.warning(f"Filter file not found: {filter_file}")
            
            # Copy only essential parts of dzx_filter folder
            dzx_filter_src = "dzx_filter"
            dzx_filter_dest = os.path.join(poe2_path, "User", "dzx_filter")
            
            if os.path.exists(dzx_filter_src):
                if os.path.exists(dzx_filter_dest):
                    shutil.rmtree(dzx_filter_dest)
                
                # Create destination directory
                os.makedirs(dzx_filter_dest, exist_ok=True)
                
                # Copy only soundeffect folder and its contents
                soundeffect_src = os.path.join(dzx_filter_src, "soundeffect")
                if os.path.exists(soundeffect_src):
                    soundeffect_dest = os.path.join(dzx_filter_dest, "soundeffect")
                    shutil.copytree(soundeffect_src, soundeffect_dest)
                    self.logger.info("Installed soundeffect folder")
                else:
                    self.logger.warning("Soundeffect folder not found")
                
                # Copy only essential files (if any)
                essential_files = []
                for file in essential_files:
                    file_src = os.path.join(dzx_filter_src, file)
                    if os.path.exists(file_src):
                        file_dest = os.path.join(dzx_filter_dest, file)
                        shutil.copy2(file_src, file_dest)
                        self.logger.info(f"Installed: {file}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error installing filters: {e}")
            return False
    
    def update_filters(self) -> bool:
        """Update filters from GitHub"""
        try:
            self.logger.info("Starting filter update...")
            
            # Download latest release
            if self.github_updater.download_latest_release():
                # Extract and install
                if self.filter_manager.extract_release():
                    poe2_path = self.find_poe2_directory()
                    if poe2_path and self.install_filters(poe2_path):
                        # Update config
                        latest_version = self.github_updater.get_latest_version()
                        self.config["current_version"] = latest_version
                        self.save_config()
                        
                        self.logger.info("Filters updated successfully")
                        return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error updating filters: {e}")
            return False
    
    def save_config(self):
        """Save configuration to file"""
        try:
            config_path = Path("config/settings.json")
            config_path.parent.mkdir(exist_ok=True)
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.error(f"Error saving config: {e}")
    
    def run(self):
        """Main installer run method"""
        try:
            self.logger.info("Starting POE2 Filter Installer...")
            
            # Check for updates
            if self.config["auto_update"] and self.check_for_updates():
                if self.update_filters():
                    self.logger.info("Installation completed with updates")
                else:
                    self.logger.error("Update failed, installing current version")
                    self.install_current_version()
            else:
                # Install current version
                self.install_current_version()
            
        except Exception as e:
            self.logger.error(f"Installer error: {e}")
            return False
        
        return True
    
    def install_current_version(self) -> bool:
        """Install current version of filters"""
        poe2_path = self.find_poe2_directory()
        if poe2_path:
            return self.install_filters(poe2_path)
        return False

def main():
    """Main entry point"""
    installer = POE2FilterInstaller()
    
    # Check if running in GUI mode
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        try:
            from gui import InstallerGUI
            gui = InstallerGUI(installer)
            gui.run()
        except ImportError as e:
            print(f"GUI not available: {e}")
            print("Running in CLI mode...")
            success = installer.run()
            if success:
                print("Installation completed successfully!")
            else:
                print("Installation failed. Check installer.log for details.")
                sys.exit(1)
    else:
        # CLI mode
        success = installer.run()
        if success:
            print("Installation completed successfully!")
        else:
            print("Installation failed. Check installer.log for details.")
            sys.exit(1)

if __name__ == "__main__":
    main()
