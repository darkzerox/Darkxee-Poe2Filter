#!/usr/bin/env python3
"""
GUI for POE2 Filter Installer
สร้าง interface สำหรับผู้ใช้
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import logging
from typing import Optional
from installer import POE2FilterInstaller

class InstallerGUI:
    """Graphical user interface for the installer"""
    
    def __init__(self, installer: POE2FilterInstaller):
        self.installer = installer
        self.logger = logging.getLogger(__name__)
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("POE2 Filter Installer")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Center window
        self.center_window()
        
        # Setup UI
        self.setup_ui()
        
        # Status variables
        self.is_installing = False
        self.is_checking_updates = False
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="POE2 Filter Installer", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Status section
        status_frame = ttk.LabelFrame(main_frame, text="สถานะการติดตั้ง", padding="10")
        status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Current version
        ttk.Label(status_frame, text="เวอร์ชันปัจจุบัน:").grid(row=0, column=0, sticky=tk.W)
        self.current_version_label = ttk.Label(status_frame, text="กำลังตรวจสอบ...")
        self.current_version_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # Latest version
        ttk.Label(status_frame, text="เวอร์ชันล่าสุด:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.latest_version_label = ttk.Label(status_frame, text="กำลังตรวจสอบ...")
        self.latest_version_label.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=(5, 0))
        
        # Update status
        ttk.Label(status_frame, text="สถานะ:").grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
        self.update_status_label = ttk.Label(status_frame, text="รอการตรวจสอบ", foreground="orange")
        self.update_status_label.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=(5, 0))
        
        # Installation section
        install_frame = ttk.LabelFrame(main_frame, text="การติดตั้ง", padding="10")
        install_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # POE2 path
        ttk.Label(install_frame, text="โฟลเดอร์ POE2:").grid(row=0, column=0, sticky=tk.W)
        self.poe2_path_var = tk.StringVar()
        self.poe2_path_entry = ttk.Entry(install_frame, textvariable=self.poe2_path_var, width=50)
        self.poe2_path_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        browse_button = ttk.Button(install_frame, text="เลือก", command=self.browse_poe2_path)
        browse_button.grid(row=0, column=2, padx=(5, 0))
        
        # Auto-detect button
        detect_button = ttk.Button(install_frame, text="ตรวจหาอัตโนมัติ", command=self.auto_detect_poe2)
        detect_button.grid(row=1, column=1, pady=(5, 0))
        
        # Buttons section
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Check updates button
        self.check_updates_button = ttk.Button(button_frame, text="ตรวจสอบอัพเดท", 
                                             command=self.check_updates)
        self.check_updates_button.grid(row=0, column=0, padx=(0, 10))
        
        # Install button
        self.install_button = ttk.Button(button_frame, text="ติดตั้ง", 
                                       command=self.install_filters)
        self.install_button.grid(row=0, column=1, padx=(0, 10))
        
        # Update button
        self.update_button = ttk.Button(button_frame, text="อัพเดท", 
                                      command=self.update_filters, state="disabled")
        self.update_button.grid(row=0, column=2, padx=(0, 10))
        
        # Progress section
        progress_frame = ttk.LabelFrame(main_frame, text="ความคืบหน้า", padding="10")
        progress_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.progress_var = tk.StringVar(value="พร้อมใช้งาน")
        self.progress_label = ttk.Label(progress_frame, textvariable=self.progress_var)
        self.progress_label.grid(row=0, column=0, sticky=tk.W)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Log section
        log_frame = ttk.LabelFrame(main_frame, text="บันทึกการทำงาน", padding="10")
        log_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.log_text = tk.Text(log_frame, height=8, width=70)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for log
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        log_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        install_frame.columnconfigure(1, weight=1)
        progress_frame.columnconfigure(0, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
        # Initial setup
        self.auto_detect_poe2()
        self.check_updates()
    
    def browse_poe2_path(self):
        """Browse for POE2 installation directory"""
        path = filedialog.askdirectory(title="เลือกโฟลเดอร์ Path of Exile 2")
        if path:
            self.poe2_path_var.set(path)
    
    def auto_detect_poe2(self):
        """Auto-detect POE2 installation directory"""
        poe2_path = self.installer.find_poe2_directory()
        if poe2_path:
            self.poe2_path_var.set(poe2_path)
            self.log_message(f"พบโฟลเดอร์ POE2: {poe2_path}")
        else:
            self.poe2_path_var.set("")
            self.log_message("ไม่พบโฟลเดอร์ POE2 กรุณาเลือกเอง")
    
    def check_updates(self):
        """Check for updates"""
        if self.is_checking_updates:
            return
        
        self.is_checking_updates = True
        self.check_updates_button.config(state="disabled")
        self.progress_var.set("กำลังตรวจสอบอัพเดท...")
        self.progress_bar.start()
        
        def check_thread():
            try:
                latest_version = self.installer.github_updater.get_latest_version()
                current_version = self.installer.config["current_version"]
                
                if latest_version:
                    self.root.after(0, lambda: self.update_version_labels(current_version, latest_version))
                    
                    if self.installer.github_updater.is_newer_version(latest_version, current_version):
                        self.root.after(0, lambda: self.enable_update_button())
                    else:
                        self.root.after(0, lambda: self.disable_update_button())
                else:
                    self.root.after(0, lambda: self.log_message("ไม่สามารถตรวจสอบอัพเดทได้"))
                    
            except Exception as e:
                self.root.after(0, lambda: self.log_message(f"ข้อผิดพลาดในการตรวจสอบอัพเดท: {e}"))
            finally:
                self.root.after(0, self.finish_check_updates)
        
        threading.Thread(target=check_thread, daemon=True).start()
    
    def update_version_labels(self, current: str, latest: str):
        """Update version labels"""
        self.current_version_label.config(text=current)
        self.latest_version_label.config(text=latest)
        
        if self.installer.github_updater.is_newer_version(latest, current):
            self.update_status_label.config(text="มีอัพเดทใหม่", foreground="green")
        else:
            self.update_status_label.config(text="เป็นเวอร์ชันล่าสุด", foreground="blue")
    
    def enable_update_button(self):
        """Enable update button"""
        self.update_button.config(state="normal")
    
    def disable_update_button(self):
        """Disable update button"""
        self.update_button.config(state="disabled")
    
    def finish_check_updates(self):
        """Finish checking updates"""
        self.is_checking_updates = False
        self.check_updates_button.config(state="normal")
        self.progress_bar.stop()
        self.progress_var.set("พร้อมใช้งาน")
    
    def install_filters(self):
        """Install filters"""
        if self.is_installing:
            return
        
        poe2_path = self.poe2_path_var.get().strip()
        if not poe2_path:
            messagebox.showerror("ข้อผิดพลาด", "กรุณาเลือกโฟลเดอร์ POE2")
            return
        
        self.is_installing = True
        self.install_button.config(state="disabled")
        self.progress_var.set("กำลังติดตั้ง...")
        self.progress_bar.start()
        
        def install_thread():
            try:
                success = self.installer.install_filters(poe2_path)
                if success:
                    self.root.after(0, lambda: self.log_message("ติดตั้งสำเร็จ"))
                    self.root.after(0, lambda: messagebox.showinfo("สำเร็จ", "ติดตั้ง filter สำเร็จ"))
                else:
                    self.root.after(0, lambda: self.log_message("ติดตั้งล้มเหลว"))
                    self.root.after(0, lambda: messagebox.showerror("ข้อผิดพลาด", "ติดตั้ง filter ล้มเหลว"))
            except Exception as e:
                self.root.after(0, lambda: self.log_message(f"ข้อผิดพลาดในการติดตั้ง: {e}"))
                self.root.after(0, lambda: messagebox.showerror("ข้อผิดพลาด", f"ข้อผิดพลาดในการติดตั้ง: {e}"))
            finally:
                self.root.after(0, self.finish_install)
        
        threading.Thread(target=install_thread, daemon=True).start()
    
    def update_filters(self):
        """Update filters"""
        if self.is_installing:
            return
        
        self.is_installing = True
        self.update_button.config(state="disabled")
        self.progress_var.set("กำลังอัพเดท...")
        self.progress_bar.start()
        
        def update_thread():
            try:
                success = self.installer.update_filters()
                if success:
                    self.root.after(0, lambda: self.log_message("อัพเดทสำเร็จ"))
                    self.root.after(0, lambda: messagebox.showinfo("สำเร็จ", "อัพเดท filter สำเร็จ"))
                    # Refresh version info
                    self.root.after(0, self.check_updates)
                else:
                    self.root.after(0, lambda: self.log_message("อัพเดทล้มเหลว"))
                    self.root.after(0, lambda: messagebox.showerror("ข้อผิดพลาด", "อัพเดท filter ล้มเหลว"))
            except Exception as e:
                self.root.after(0, lambda: self.log_message(f"ข้อผิดพลาดในการอัพเดท: {e}"))
                self.root.after(0, lambda: messagebox.showerror("ข้อผิดพลาด", f"ข้อผิดพลาดในการอัพเดท: {e}"))
            finally:
                self.root.after(0, self.finish_install)
        
        threading.Thread(target=update_thread, daemon=True).start()
    
    def finish_install(self):
        """Finish installation/update"""
        self.is_installing = False
        self.install_button.config(state="normal")
        self.update_button.config(state="normal")
        self.progress_bar.stop()
        self.progress_var.set("พร้อมใช้งาน")
    
    def log_message(self, message: str):
        """Add message to log"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
    
    def run(self):
        """Run the GUI"""
        try:
            self.root.mainloop()
        except Exception as e:
            self.logger.error(f"GUI error: {e}")
            messagebox.showerror("ข้อผิดพลาด", f"ข้อผิดพลาดใน GUI: {e}")
