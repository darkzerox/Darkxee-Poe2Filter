#!/usr/bin/env python3
"""
DZX PoE2 Filter Installer & Launcher (with Auto-Updater)
=======================================================

A Tkinter-based graphical installer for easy deployment of DZX POE2 filters
to the local game directory. It automatically checks for and downloads the
latest compiled filters directly from GitHub releases.

Author: Darkxee
License: MIT
"""

import os
import sys
import json
import shutil
import ctypes
import urllib.request
import zipfile
import io
import threading
from ctypes import wintypes
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser

# Target game directory name
GAME_DIR_NAME = Path("My Games") / "Path of Exile 2"

def get_documents_folder() -> Path:
    """Get the user's Documents folder path reliably on Windows, handling redirects"""
    if sys.platform == 'win32':
        try:
            # CSIDL_PERSONAL = 5 is the My Documents folder
            buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
            ctypes.windll.shell32.SHGetFolderPathW(None, 5, None, 0, buf)
            return Path(buf.value)
        except Exception:
            pass
    # Fallback for other OS or if ctypes fails
    return Path(os.path.expanduser('~')) / 'Documents'

def get_default_target_dir() -> Path:
    """Return the default Path of Exile 2 filter folder"""
    return get_documents_folder() / GAME_DIR_NAME

class FilterInstallerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DZX PoE2 Filter Installer & Launcher")
        self.root.geometry("540x450")
        self.root.configure(bg="#0f0f0f")
        self.root.resizable(False, False)
        
        # Determine resource path (where bundled files are located)
        if getattr(sys, 'frozen', False):
            self.base_path = Path(sys._MEIPASS)
        else:
            self.base_path = Path(__file__).parent.parent
            
        self.filters_src = self.base_path / "filters"
        # In development mode, check if we need to fall back to dist/filter
        if not self.filters_src.exists():
            self.filters_src = self.base_path / "dist" / "filter"
            
        self.target_dir = tk.StringVar(value=str(get_default_target_dir()))
        self.target_dir.trace_add("write", lambda *args: self.update_installed_version_display())
        
        # Versioning Variables
        self.installed_version_str = tk.StringVar(value="กำลังตรวจสอบ...")
        self.latest_version_str = tk.StringVar(value="กำลังตรวจสอบ...")
        self.bundled_version = "0.5.1"
        self.online_zip_url = None
        self.latest_tag = None
        
        # Create UI
        self.create_widgets()
        
        # Start background update check
        threading.Thread(target=self.check_updates_thread, daemon=True).start()
        
    def create_widgets(self):
        # Header / Banner
        header_frame = tk.Frame(self.root, bg="#1a1a1a", height=80)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)
        
        # Try to load and display logo if it exists in base path
        logo_path = self.base_path / "dzx_filter" / "images" / "dzx-poe2-filter-logo.png"
        logo_loaded = False
        if logo_path.exists():
            try:
                self.logo_img = tk.PhotoImage(file=str(logo_path))
                logo_label = tk.Label(header_frame, image=self.logo_img, bg="#1a1a1a")
                logo_label.pack(pady=10)
                logo_loaded = True
            except Exception:
                pass
                
        if not logo_loaded:
            # Text-based header fallback
            title_label = tk.Label(
                header_frame, 
                text="DZX FILTER POE2", 
                font=("Helvetica", 20, "bold"), 
                fg="#d4b26f", 
                bg="#1a1a1a"
            )
            title_label.pack(pady=12)
            subtitle_label = tk.Label(
                header_frame, 
                text="Item Filter Installer & Launcher", 
                font=("Helvetica", 9), 
                fg="#888888", 
                bg="#1a1a1a"
            )
            subtitle_label.pack(side="top", pady=(0, 5))

        # Main Body Frame
        body_frame = tk.Frame(self.root, bg="#0f0f0f", padx=25, pady=15)
        body_frame.pack(fill="both", expand=True)
        
        # Description
        desc_text = "โปรแกรมช่วยติดตั้ง Item Filter สำหรับเกม Path of Exile 2 ลงเครื่องคอมพิวเตอร์ของคุณอัตโนมัติ"
        desc_label = tk.Label(
            body_frame,
            text=desc_text,
            font=("Leelawadee UI", 10),
            fg="#cccccc",
            bg="#0f0f0f",
            wraplength=480,
            justify="center"
        )
        desc_label.pack(pady=(0, 10))
        
        # Version Info Box
        version_frame = tk.Frame(body_frame, bg="#141414", bd=1, relief="solid", padx=15, pady=8)
        version_frame.pack(fill="x", pady=(0, 12))
        
        # Installed Version Row
        installed_title = tk.Label(
            version_frame,
            text="เวอร์ชันที่ติดตั้งอยู่:",
            font=("Leelawadee UI", 9),
            fg="#888888",
            bg="#141414"
        )
        installed_title.grid(row=0, column=0, sticky="w", pady=2)
        
        self.installed_val_label = tk.Label(
            version_frame,
            textvariable=self.installed_version_str,
            font=("Consolas", 10, "bold"),
            fg="#ffffff",
            bg="#141414"
        )
        self.installed_val_label.grid(row=0, column=1, sticky="w", padx=(15, 0), pady=2)
        
        # Latest Version Row
        latest_title = tk.Label(
            version_frame,
            text="เวอร์ชันล่าสุดออนไลน์:",
            font=("Leelawadee UI", 9),
            fg="#888888",
            bg="#141414"
        )
        latest_title.grid(row=1, column=0, sticky="w", pady=2)
        
        self.latest_val_label = tk.Label(
            version_frame,
            textvariable=self.latest_version_str,
            font=("Consolas", 10, "bold"),
            fg="#d4b26f",
            bg="#141414"
        )
        self.latest_val_label.grid(row=1, column=1, sticky="w", padx=(15, 0), pady=2)
        
        # Path Selection Label
        path_label = tk.Label(
            body_frame,
            text="โฟลเดอร์สำหรับติดตั้ง (หากไม่ระบุ จะติดตั้งที่ My Documents\\Path of Exile 2\\Filters)",
            font=("Leelawadee UI", 9, "bold"),
            fg="#a0a0a0",
            bg="#0f0f0f"
        )
        path_label.pack(anchor="w", pady=(0, 5))
        
        # Path Entry & Browse Frame
        path_frame = tk.Frame(body_frame, bg="#0f0f0f")
        path_frame.pack(fill="x", pady=(0, 15))
        
        self.path_entry = tk.Entry(
            path_frame,
            textvariable=self.target_dir,
            font=("Consolas", 9),
            bg="#1f1f1f",
            fg="#ffffff",
            insertbackground="#ffffff",
            bd=1,
            relief="flat",
            state="readonly"
        )
        self.path_entry.pack(side="left", fill="x", expand=True, ipady=4, padx=(0, 5))
        
        browse_btn = tk.Button(
            path_frame,
            text="เลือกโฟลเดอร์...",
            font=("Leelawadee UI", 9),
            bg="#2c2c2c",
            fg="#ffffff",
            activebackground="#3d3d3d",
            activeforeground="#ffffff",
            bd=0,
            padx=10,
            pady=3,
            command=self.browse_folder
        )
        browse_btn.pack(side="right")
        
        # Install Button
        self.install_btn = tk.Button(
            body_frame,
            text="กำลังตรวจสอบเวอร์ชัน...",
            font=("Leelawadee UI", 12, "bold"),
            bg="#d4b26f",
            fg="#0f0f0f",
            activebackground="#b08f4f",
            activeforeground="#0f0f0f",
            bd=0,
            cursor="hand2",
            state="disabled",
            command=self.start_install
        )
        self.install_btn.pack(fill="x", ipady=8, pady=(0, 10))
        
        # Status Label
        self.status_label = tk.Label(
            body_frame,
            text="ระบบกำลังเตรียมข้อมูล...",
            font=("Leelawadee UI", 9),
            fg="#888888",
            bg="#0f0f0f"
        )
        self.status_label.pack(pady=(0, 10))
        
        # Separator Line
        separator = tk.Frame(body_frame, bg="#2a2a2a", height=1)
        separator.pack(fill="x", pady=(0, 12))
        
        # Footer Action Buttons
        footer_frame = tk.Frame(body_frame, bg="#0f0f0f")
        footer_frame.pack(fill="x")
        
        open_folder_btn = tk.Button(
            footer_frame,
            text="📁 เปิดโฟลเดอร์ Filter",
            font=("Leelawadee UI", 9),
            bg="#1f1f1f",
            fg="#cccccc",
            activebackground="#2c2c2c",
            activeforeground="#ffffff",
            bd=0,
            padx=10,
            pady=5,
            command=self.open_target_folder
        )
        open_folder_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        play_btn = tk.Button(
            footer_frame,
            text="🎮 เข้าเล่นเกม POE2 (Steam)",
            font=("Leelawadee UI", 9, "bold"),
            bg="#1f3d24",
            fg="#81c784",
            activebackground="#2e5c35",
            activeforeground="#ffffff",
            bd=0,
            padx=10,
            pady=5,
            command=self.launch_game
        )
        play_btn.pack(side="right", fill="x", expand=True, padx=(5, 0))
        
    def check_updates_thread(self):
        """Read versions and request GitHub release info in background"""
        # 1. Read bundled version
        try:
            config_path = self.base_path / "config.json"
            if config_path.exists():
                with open(config_path, "r", encoding="utf-8") as f:
                    config_data = json.load(f)
                    self.bundled_version = config_data.get("project", {}).get("version", "0.5.1")
        except Exception:
            pass
            
        # Update installed display
        self.update_installed_version_display()
        
        # 2. Check online version
        try:
            req = urllib.request.Request(
                'https://api.github.com/repos/darkzerox/Darkxee-Poe2Filter/releases/latest',
                headers={'User-Agent': 'DZX-Filter-Launcher'}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                self.latest_tag = data.get('tag_name')
                
                # Extract clean version number
                self.latest_version_str.set(f"{self.latest_tag} (GitHub)")
                
                # Find zip asset
                assets = data.get('assets', [])
                for asset in assets:
                    if asset.get('name') == 'dzx-poe2-filter.zip':
                        self.online_zip_url = asset.get('browser_download_url')
                        break
        except Exception:
            # Fallback to offline
            self.latest_version_str.set(f"v{self.bundled_version} (ในเครื่อง / Offline)")
            self.latest_tag = f"v{self.bundled_version}"
            self.online_zip_url = None
            
        # Update button and status
        self.root.after(0, self.on_check_completed)
        
    def on_check_completed(self):
        """Called on main UI thread once check finishes"""
        installed = self.installed_version_str.get().lstrip('v')
        latest = self.latest_tag.lstrip('v') if self.latest_tag else self.bundled_version
        
        if self.online_zip_url:
            if installed != latest:
                self.install_btn.config(text=f"ดาวน์โหลด & อัปเดตเป็น {self.latest_tag} (GitHub)", state="normal", bg="#d4b26f")
                self.status_label.config(text="✨ มีฟิลเตอร์เวอร์ชันใหม่พร้อมให้อัปเดต!", fg="#81c784")
            else:
                self.install_btn.config(text="ติดตั้งฟิลเตอร์ใหม่ / ติดตั้งซ้ำ", state="normal", bg="#d4b26f")
                self.status_label.config(text="✅ ฟิลเตอร์ของคุณเป็นเวอร์ชันล่าสุดแล้ว", fg="#4caf50")
        else:
            self.install_btn.config(text=f"ติดตั้งแบบ Offline (v{self.bundled_version})", state="normal", bg="#d4b26f")
            self.status_label.config(text="⚠️ ทำงานในโหมด Offline (จะติดตั้งฟิลเตอร์ที่มีอยู่ในตัวโปรแกรม)", fg="#ff9800")
            
    def update_installed_version_display(self):
        """Reads installed version and updates the label string"""
        dest_path = Path(self.target_dir.get())
        ver_file = dest_path / ".installed_version"
        installed_ver = "ไม่ได้ติดตั้ง"
        if ver_file.exists():
            try:
                with open(ver_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    installed_ver = f"v{data.get('version', '')}"
            except Exception:
                pass
        self.installed_version_str.set(installed_ver)
        
    def browse_folder(self):
        selected = filedialog.askdirectory(
            initialdir=self.target_dir.get(),
            title="เลือกโฟลเดอร์ติดตั้งฟิลเตอร์ Path of Exile 2"
        )
        if selected:
            normalized = str(Path(selected))
            self.target_dir.set(normalized)
            
    def start_install(self):
        """Disable buttons and spin up the install thread"""
        self.install_btn.config(state="disabled")
        self.status_label.config(text="⏳ เริ่มต้นการติดตั้ง...", fg="#d4b26f")
        threading.Thread(target=self.install_thread, daemon=True).start()
        
    def install_thread(self):
        """Runs the download or local copy on a background thread"""
        dest_path = Path(self.target_dir.get())
        
        try:
            dest_path.mkdir(parents=True, exist_ok=True)
            version_installed = None
            
            # Case 1: Download from GitHub
            if self.online_zip_url:
                self.show_status(f"⏳ กำลังดาวน์โหลดเวอร์ชัน {self.latest_tag} จาก GitHub...", "#d4b26f")
                
                req = urllib.request.Request(
                    self.online_zip_url,
                    headers={'User-Agent': 'DZX-Filter-Launcher'}
                )
                with urllib.request.urlopen(req, timeout=15) as response:
                    zip_data = response.read()
                    
                self.show_status("⏳ กำลังแตกไฟล์ฟิลเตอร์ไปยังโฟลเดอร์เกม...", "#d4b26f")
                with zipfile.ZipFile(io.BytesIO(zip_data)) as zip_ref:
                    zip_ref.extractall(dest_path)
                    
                version_installed = self.latest_tag.lstrip('v')
                self.show_status(f"✅ ติดตั้งฟิลเตอร์ v{version_installed} สำเร็จ!", "#4caf50")
                
            # Case 2: Offline fallback / Local Copy
            else:
                self.show_status(f"⏳ กำลังติดตั้งฟิลเตอร์ในเครื่อง (v{self.bundled_version}) แบบ Offline...", "#d4b26f")
                
                if not self.filters_src.exists():
                    self.show_status("❌ ไม่พบไฟล์ฟิลเตอร์ต้นฉบับ", "#f44336")
                    messagebox.showerror("Error", "ไม่พบไฟล์ฟิลเตอร์ในตัวโปรแกรม และไม่สามารถเชื่อมต่ออินเทอร์เน็ตได้")
                    return
                    
                # Copy filter files
                filter_count = 0
                for item in self.filters_src.iterdir():
                    if item.is_file() and item.suffix == '.filter':
                        shutil.copy2(item, dest_path / item.name)
                        filter_count += 1
                        
                # Copy sound effects
                src_sound = self.filters_src / "dzx_filter" / "soundeffect"
                if src_sound.exists():
                    dest_sound = dest_path / "dzx_filter" / "soundeffect"
                    if dest_sound.exists():
                        shutil.rmtree(dest_sound)
                    shutil.copytree(src_sound, dest_sound)
                    
                version_installed = self.bundled_version
                self.show_status(f"✅ ติดตั้งฟิลเตอร์ v{version_installed} (Offline) สำเร็จ!", "#4caf50")
                
            # Write installed version marker
            ver_file = dest_path / ".installed_version"
            with open(ver_file, "w", encoding="utf-8") as f:
                json.dump({"version": version_installed}, f, ensure_ascii=False, indent=2)
                
            # Update display values
            self.update_installed_version_display()
            self.root.after(0, self.on_check_completed)
            messagebox.showinfo("Success", f"ติดตั้งฟิลเตอร์ DZX POE2 เรียบร้อยแล้ว!\nเวอร์ชัน: v{version_installed}")
            
        except Exception as e:
            self.show_status(f"❌ เกิดข้อผิดพลาด: {str(e)}", "#f44336")
            messagebox.showerror("Error", f"ไม่สามารถติดตั้งฟิลเตอร์ได้เนื่องจาก:\n{str(e)}")
            
        finally:
            self.install_btn.config(state="normal")
            
    def open_target_folder(self):
        dest_path = self.target_dir.get()
        if os.path.exists(dest_path):
            os.startfile(dest_path)
        else:
            try:
                os.makedirs(dest_path, exist_ok=True)
                os.startfile(dest_path)
            except Exception as e:
                messagebox.showerror("Error", f"ไม่สามารถเปิดโฟลเดอร์ได้: {str(e)}")
                
    def launch_game(self):
        try:
            webbrowser.open("steam://rungameid/2694490")
            self.show_status("🎮 กำลังสั่งเปิดเกม Path of Exile 2 ผ่าน Steam...", "#81c784")
        except Exception as e:
            messagebox.showerror("Error", f"ไม่สามารถรันเกมได้: {str(e)}")
            
    def show_status(self, text, color):
        self.root.after(0, lambda: self.status_label.config(text=text, fg=color))
        
if __name__ == "__main__":
    if sys.platform == 'win32':
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            try:
                ctypes.windll.user32.SetProcessDPIAware();
            except Exception:
                pass
                
    root = tk.Tk()
    app = FilterInstallerGUI(root)
    root.mainloop()
