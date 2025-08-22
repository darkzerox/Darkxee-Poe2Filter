#!/usr/bin/env python3
"""
Filter Manager for POE2 Filter Installer
จัดการการติดตั้ง, อัพเดท และ rollback ของ filter files
"""

import os
import shutil
import zipfile
import logging
import hashlib
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from datetime import datetime

class FilterManager:
    """Manages filter installation and updates"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.backup_dir = "backups"
        self.temp_dir = "temp"
        self.ensure_directories()
    
    def ensure_directories(self):
        """Ensure necessary directories exist"""
        for directory in [self.backup_dir, self.temp_dir]:
            os.makedirs(directory, exist_ok=True)
    
    def create_backup(self, poe2_path: str) -> Optional[str]:
        """Create backup of current filters"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"filter_backup_{timestamp}"
            backup_path = os.path.join(self.backup_dir, backup_name)
            
            # Backup filters directory (only essential filters)
            filters_src = os.path.join(poe2_path, "User", "Filters")
            filters_backup = os.path.join(backup_path, "Filters")
            
            if os.path.exists(filters_src):
                os.makedirs(filters_backup, exist_ok=True)
                
                # Backup only essential filter files
                essential_filters = ["dzx-poe2.filter"]
                import glob
                additional_filters = glob.glob(os.path.join(filters_src, "dzx-poe2-*.filter"))
                essential_filters.extend([os.path.basename(f) for f in additional_filters])
                
                for filter_file in essential_filters:
                    filter_src = os.path.join(filters_src, filter_file)
                    if os.path.exists(filter_src):
                        filter_dest = os.path.join(filters_backup, filter_file)
                        shutil.copy2(filter_src, filter_dest)
                
                self.logger.info(f"Backed up essential filters to: {filters_backup}")
            
            # Backup only essential parts of dzx_filter directory
            dzx_filter_src = os.path.join(poe2_path, "User", "dzx_filter")
            dzx_filter_backup = os.path.join(backup_path, "dzx_filter")
            
            if os.path.exists(dzx_filter_src):
                os.makedirs(dzx_filter_backup, exist_ok=True)
                
                # Backup only soundeffect folder
                soundeffect_src = os.path.join(dzx_filter_src, "soundeffect")
                if os.path.exists(soundeffect_src):
                    soundeffect_backup = os.path.join(dzx_filter_backup, "soundeffect")
                    shutil.copytree(soundeffect_src, soundeffect_backup)
                    self.logger.info(f"Backed up soundeffect to: {soundeffect_backup}")
            
            # Create backup info file
            backup_info = {
                "timestamp": timestamp,
                "poe2_path": poe2_path,
                "backup_path": backup_path,
                "filters_count": len(essential_filters),
                "soundeffect_backed_up": os.path.exists(soundeffect_src) if 'soundeffect_src' in locals() else False
            }
            
            info_file = os.path.join(backup_path, "backup_info.json")
            import json
            with open(info_file, 'w', encoding='utf-8') as f:
                json.dump(backup_info, f, indent=2, ensure_ascii=False)
            
            return backup_path
            
        except Exception as e:
            self.logger.error(f"Error creating backup: {e}")
            return None
    
    def restore_backup(self, backup_path: str, poe2_path: str) -> bool:
        """Restore filters from backup"""
        try:
            # Restore filters (only essential filters)
            filters_backup = os.path.join(backup_path, "Filters")
            filters_dest = os.path.join(poe2_path, "User", "Filters")
            
            if os.path.exists(filters_backup):
                if os.path.exists(filters_dest):
                    shutil.rmtree(filters_dest)
                os.makedirs(filters_dest, exist_ok=True)
                
                # Restore only essential filter files
                for filter_file in os.listdir(filters_backup):
                    if filter_file.startswith("dzx-poe2"):
                        filter_src = os.path.join(filters_backup, filter_file)
                        filter_dest_file = os.path.join(filters_dest, filter_file)
                        shutil.copy2(filter_src, filter_dest_file)
                
                self.logger.info(f"Restored essential filters from: {filters_backup}")
            
            # Restore only essential parts of dzx_filter
            dzx_filter_backup = os.path.join(backup_path, "dzx_filter")
            dzx_filter_dest = os.path.join(poe2_path, "User", "dzx_filter")
            
            if os.path.exists(dzx_filter_backup):
                if os.path.exists(dzx_filter_dest):
                    shutil.rmtree(dzx_filter_dest)
                os.makedirs(dzx_filter_dest, exist_ok=True)
                
                # Restore only soundeffect folder
                soundeffect_backup = os.path.join(dzx_filter_backup, "soundeffect")
                if os.path.exists(soundeffect_backup):
                    soundeffect_dest = os.path.join(dzx_filter_dest, "soundeffect")
                    shutil.copytree(soundeffect_backup, soundeffect_dest)
                    self.logger.info(f"Restored soundeffect from: {soundeffect_backup}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error restoring backup: {e}")
            return False
    
    def extract_release(self, zip_file: str) -> bool:
        """Extract release zip file"""
        try:
            if not os.path.exists(zip_file):
                self.logger.error(f"Zip file not found: {zip_file}")
                return False
            
            # Clear temp directory
            temp_path = Path(self.temp_dir)
            for item in temp_path.iterdir():
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
            
            # Extract zip file
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(self.temp_dir)
            
            self.logger.info(f"Extracted release: {zip_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error extracting release: {e}")
            return False
    
    def get_directory_size(self, directory: str) -> int:
        """Get total size of directory in bytes"""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    if os.path.exists(filepath):
                        total_size += os.path.getsize(filepath)
        except Exception as e:
            self.logger.error(f"Error calculating directory size: {e}")
        
        return total_size
    
    def calculate_checksum(self, file_path: str) -> Optional[str]:
        """Calculate SHA256 checksum of file"""
        try:
            sha256_hash = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(chunk)
            return sha256_hash.hexdigest()
        except Exception as e:
            self.logger.error(f"Error calculating checksum: {e}")
            return None
    
    def verify_checksum(self, file_path: str, expected_checksum: str) -> bool:
        """Verify file checksum"""
        actual_checksum = self.calculate_checksum(file_path)
        if actual_checksum:
            return actual_checksum == expected_checksum
        return False
    
    def list_backups(self) -> List[Dict]:
        """List available backups"""
        backups = []
        try:
            for item in os.listdir(self.backup_dir):
                backup_path = os.path.join(self.backup_dir, item)
                if os.path.isdir(backup_path):
                    info_file = os.path.join(backup_path, "backup_info.json")
                    if os.path.exists(info_file):
                        import json
                        with open(info_file, 'r', encoding='utf-8') as f:
                            backup_info = json.load(f)
                            backups.append(backup_info)
        except Exception as e:
            self.logger.error(f"Error listing backups: {e}")
        
        # Sort by timestamp (newest first)
        backups.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        return backups
    
    def cleanup_old_backups(self, keep_count: int = 5):
        """Remove old backups, keeping only the specified number"""
        try:
            backups = self.list_backups()
            if len(backups) > keep_count:
                backups_to_remove = backups[keep_count:]
                
                for backup in backups_to_remove:
                    backup_path = backup.get('backup_path')
                    if backup_path and os.path.exists(backup_path):
                        shutil.rmtree(backup_path)
                        self.logger.info(f"Removed old backup: {backup_path}")
                        
        except Exception as e:
            self.logger.error(f"Error cleaning up old backups: {e}")
    
    def get_installation_status(self, poe2_path: str) -> Dict:
        """Get current installation status"""
        status = {
            "essential_filters_installed": False,
            "soundeffect_installed": False,
            "essential_filters_count": 0,
            "soundeffect_size": 0,
            "last_modified": None
        }
        
        try:
            # Check essential filters
            filters_dir = os.path.join(poe2_path, "User", "Filters")
            if os.path.exists(filters_dir):
                # Count only essential filter files
                essential_filters = []
                for file in os.listdir(filters_dir):
                    if file.startswith("dzx-poe2"):
                        essential_filters.append(file)
                
                if essential_filters:
                    status["essential_filters_installed"] = True
                    status["essential_filters_count"] = len(essential_filters)
                    
                    # Get last modified time
                    mtime = os.path.getmtime(filters_dir)
                    status["last_modified"] = datetime.fromtimestamp(mtime).isoformat()
            
            # Check soundeffect folder
            soundeffect_dir = os.path.join(poe2_path, "User", "dzx_filter", "soundeffect")
            if os.path.exists(soundeffect_dir):
                status["soundeffect_installed"] = True
                status["soundeffect_size"] = self.get_directory_size(soundeffect_dir)
            
        except Exception as e:
            self.logger.error(f"Error getting installation status: {e}")
        
        return status
