#!/usr/bin/env python3
"""
GitHub Updater for POE2 Filter Installer
จัดการการเช็ค version และดาวน์โหลดจาก GitHub
"""

import os
import requests
import logging
from typing import Optional, Dict, List
from packaging import version

class GitHubUpdater:
    """GitHub API updater for filters"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.api_base = "https://api.github.com"
        self.repo = "your-username/dzx-filter-poe2"  # เปลี่ยนเป็น repo ของคุณ
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'POE2-Filter-Installer/1.0',
            'Accept': 'application/vnd.github.v3+json'
        })
    
    def get_latest_release(self) -> Optional[str]:
        """Get latest release version from GitHub"""
        try:
            url = f"{self.api_base}/repos/{self.repo}/releases/latest"
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            release_data = response.json()
            latest_version = release_data['tag_name'].lstrip('v')
            
            self.logger.info(f"Latest release version: {latest_version}")
            return latest_version
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching latest release: {e}")
            return None
        except KeyError as e:
            self.logger.error(f"Error parsing release data: {e}")
            return None
    
    def get_release_assets(self, version_tag: str) -> List[Dict]:
        """Get assets for specific release version"""
        try:
            url = f"{self.api_base}/repos/{self.repo}/releases/tags/v{version_tag}"
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            release_data = response.json()
            assets = release_data.get('assets', [])
            
            self.logger.info(f"Found {len(assets)} assets for version {version_tag}")
            return assets
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching release assets: {e}")
            return []
    
    def download_asset(self, asset_url: str, filename: str) -> bool:
        """Download specific asset from GitHub"""
        try:
            headers = {
                'Accept': 'application/octet-stream',
                'User-Agent': 'POE2-Filter-Installer/1.0'
            }
            
            response = self.session.get(asset_url, headers=headers, stream=True, timeout=60)
            response.raise_for_status()
            
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            self.logger.info(f"Downloaded: {filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error downloading asset: {e}")
            return False
    
    def download_latest_release(self) -> bool:
        """Download latest release zip file"""
        try:
            latest_version = self.get_latest_release()
            if not latest_version:
                return False
            
            assets = self.get_release_assets(latest_version)
            
            # Find zip file
            zip_asset = None
            for asset in assets:
                if asset['name'].endswith('.zip'):
                    zip_asset = asset
                    break
            
            if not zip_asset:
                self.logger.error("No zip file found in release")
                return False
            
            # Download zip file
            filename = f"dzx-filter-poe2-v{latest_version}.zip"
            if self.download_asset(zip_asset['browser_download_url'], filename):
                self.logger.info(f"Successfully downloaded {filename}")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error downloading latest release: {e}")
            return False
    
    def is_newer_version(self, new_version: str, current_version: str) -> bool:
        """Check if new version is newer than current"""
        try:
            return version.parse(new_version) > version.parse(current_version)
        except version.InvalidVersion as e:
            self.logger.error(f"Invalid version format: {e}")
            return False
    
    def get_release_notes(self, version_tag: str) -> Optional[str]:
        """Get release notes for specific version"""
        try:
            url = f"{self.api_base}/repos/{self.repo}/releases/tags/v{version_tag}"
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            release_data = response.json()
            return release_data.get('body', '')
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching release notes: {e}")
            return None
    
    def check_connection(self) -> bool:
        """Check if GitHub API is accessible"""
        try:
            response = self.session.get(f"{self.api_base}/rate_limit", timeout=10)
            return response.status_code == 200
        except:
            return False
