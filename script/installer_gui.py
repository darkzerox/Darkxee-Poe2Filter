#!/usr/bin/env python3
"""
DZX PoE2 Filter Installer & Launcher
===================================

A Tkinter-based graphical installer for easy deployment of DZX POE2 filters
to the local game directory.

Author: Darkxee
License: MIT
"""

import os
import sys
import shutil
import ctypes
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
        self.root.geometry("540x420")
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
        
        # Create UI
        self.create_widgets()
        
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
                # Scale image if needed (Tkinter PhotoImage lacks easy scaling, so we just display it if it fits)
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
        body_frame = tk.Frame(self.root, bg="#0f0f0f", padx=25, pady=20)
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
        desc_label.pack(pady=(0, 15))
        
        # Path Selection Label
        path_label = tk.Label(
            body_frame,
            text="โฟลเดอร์สำหรับติดตั้ง Filter (Target Folder):",
            font=("Leelawadee UI", 9, "bold"),
            fg="#a0a0a0",
            bg="#0f0f0f"
        )
        path_label.pack(anchor="w", pady=(0, 5))
        
        # Path Entry & Browse Frame
        path_frame = tk.Frame(body_frame, bg="#0f0f0f")
        path_frame.pack(fill="x", pady=(0, 20))
        
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
            text="ติดตั้ง / อัปเดต Filter",
            font=("Leelawadee UI", 12, "bold"),
            bg="#d4b26f",
            fg="#0f0f0f",
            activebackground="#b08f4f",
            activeforeground="#0f0f0f",
            bd=0,
            cursor="hand2",
            command=self.start_install
        )
        self.install_btn.pack(fill="x", ipady=8, pady=(0, 15))
        
        # Status Label
        self.status_label = tk.Label(
            body_frame,
            text="ระบบพร้อมสำหรับการติดตั้ง...",
            font=("Leelawadee UI", 9),
            fg="#888888",
            bg="#0f0f0f"
        )
        self.status_label.pack(pady=(0, 15))
        
        # Separator Line
        separator = tk.Frame(body_frame, bg="#2a2a2a", height=1)
        separator.pack(fill="x", pady=(0, 15))
        
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
        
    def browse_folder(self):
        selected = filedialog.askdirectory(
            initialdir=self.target_dir.get(),
            title="เลือกโฟลเดอร์ติดตั้งฟิลเตอร์ Path of Exile 2"
        )
        if selected:
            # Ensure path uses standard OS separator
            normalized = str(Path(selected))
            self.target_dir.set(normalized)
            
    def start_install(self):
        dest_path = Path(self.target_dir.get())
        
        # Verification
        if not self.filters_src.exists():
            self.show_status("❌ ไม่พบไฟล์ฟิลเตอร์ต้นฉบับกรุณา Build ก่อนสร้าง Launcher", "#f44336")
            messagebox.showerror("Error", "ไม่พบไฟล์ฟิลเตอร์ต้นฉบับในโฟลเดอร์ที่กำหนด (กรุณารัน start_build.py ก่อน)")
            return
            
        self.show_status("⏳ กำลังลบฟิลเตอร์เก่าและลงฟิลเตอร์ใหม่...", "#d4b26f")
        self.root.update_idletasks()
        
        try:
            # Create game directory structure
            dest_path.mkdir(parents=True, exist_ok=True)
            
            # Count copied items
            filter_count = 0
            
            # Copy filter files
            for item in self.filters_src.iterdir():
                if item.is_file() and item.suffix == '.filter':
                    shutil.copy2(item, dest_path / item.name)
                    filter_count += 1
                    
            # Copy sound effect folder
            src_sound = self.filters_src / "dzx_filter" / "soundeffect"
            if src_sound.exists():
                dest_sound = dest_path / "dzx_filter" / "soundeffect"
                if dest_sound.exists():
                    shutil.rmtree(dest_sound)
                shutil.copytree(src_sound, dest_sound)
                
            self.show_status(f"✅ ติดตั้งฟิลเตอร์สำเร็จ! ทั้งหมด {filter_count} รูปแบบ", "#4caf50")
            messagebox.showinfo("Success", f"ติดตั้งฟิลเตอร์เรียบร้อยแล้ว!\nจำนวน {filter_count} ไฟล์ฟิลเตอร์ + ไฟล์เสียงแจ้งเตือน")
            
        except Exception as e:
            self.show_status(f"❌ เกิดข้อผิดพลาด: {str(e)}", "#f44336")
            messagebox.showerror("Error", f"ไม่สามารถติดตั้งฟิลเตอร์ได้เนื่องจาก:\n{str(e)}")
            
    def open_target_folder(self):
        dest_path = self.target_dir.get()
        if os.path.exists(dest_path):
            os.startfile(dest_path)
        else:
            # If path doesn't exist, create it first
            try:
                os.makedirs(dest_path, exist_ok=True)
                os.startfile(dest_path)
            except Exception as e:
                messagebox.showerror("Error", f"ไม่สามารถเปิดโฟลเดอร์ได้: {str(e)}")
                
    def launch_game(self):
        try:
            # Launch POE2 via Steam protocol
            webbrowser.open("steam://rungameid/2694490")
            self.show_status("🎮 กำลังสั่งเปิดเกม Path of Exile 2 ผ่าน Steam...", "#81c784")
        except Exception as e:
            messagebox.showerror("Error", f"ไม่สามารถรันเกมได้: {str(e)}")
            
    def show_status(self, text, color):
        self.status_label.config(text=text, fg=color)
        
if __name__ == "__main__":
    # Request high DPI awareness on Windows for crisp fonts
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
