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
        
        # Bind path change event
        self.poe2_path_var.trace('w', lambda *args: self.update_path_status())
        
        browse_button = ttk.Button(install_frame, text="เลือก", command=self.browse_poe2_path)
        browse_button.grid(row=0, column=2, padx=(5, 0))
        
        # Default paths info
        default_paths_frame = ttk.Frame(install_frame)
        default_paths_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))
        
        ttk.Label(default_paths_frame, text="Default paths:", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky=tk.W)
        
        # Show default paths
        default_paths = self.installer.poe2_paths
        for i, path in enumerate(default_paths):
            path_label = ttk.Label(default_paths_frame, text=f"  {i+1}. {path}", font=("Arial", 8))
            path_label.grid(row=i+1, column=0, sticky=tk.W, padx=(20, 0))
            
            # Add button to use this path
            use_path_button = ttk.Button(default_paths_frame, text="ใช้", 
                                       command=lambda p=path: self.use_default_path(p))
            use_path_button.grid(row=i+1, column=1, padx=(10, 0))
        
        # Auto-detect button
        detect_button = ttk.Button(install_frame, text="ตรวจหาอัตโนมัติ", command=self.auto_detect_poe2)
        detect_button.grid(row=2, column=1, pady=(5, 0))
        
        # Path status
        self.path_status_var = tk.StringVar(value="ยังไม่ได้เลือกโฟลเดอร์")
        self.path_status_label = ttk.Label(install_frame, textvariable=self.path_status_var, 
                                         foreground="orange", font=("Arial", 9))
        self.path_status_label.grid(row=3, column=0, columnspan=3, sticky=tk.W, pady=(5, 0))
        
        # Validate path button
        validate_button = ttk.Button(install_frame, text="ตรวจสอบโฟลเดอร์", command=self.validate_current_path)
        validate_button.grid(row=4, column=1, pady=(5, 0))
        
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
            self.log_message(f"เลือกโฟลเดอร์: {path}")
            
            # Validate if this looks like a POE2 directory
            if self.validate_poe2_directory(path):
                self.log_message("✅ โฟลเดอร์นี้ดูเหมือนจะเป็น POE2 directory")
            else:
                self.log_message("⚠️  โฟลเดอร์นี้อาจไม่ใช่ POE2 directory")
            
            # Update status
            self.update_path_status()
    
    def use_default_path(self, path):
        """Use one of the default paths"""
        self.poe2_path_var.set(path)
        self.log_message(f"ใช้ default path: {path}")
        
        # Validate the path
        if os.path.exists(path):
            self.log_message("✅ โฟลเดอร์มีอยู่จริง")
        else:
            self.log_message("⚠️  โฟลเดอร์ไม่มีอยู่ จะสร้างให้อัตโนมัติ")
        
        # Update status
        self.update_path_status()
    
    def validate_poe2_directory(self, path):
        """Validate if the directory looks like a POE2 installation"""
        try:
            # Check if it contains common POE2 directories/files
            poe2_indicators = [
                "User",
                "User/Filters",
                "User/Config",
                "User/Logs"
            ]
            
            for indicator in poe2_indicators:
                indicator_path = os.path.join(path, indicator)
                if os.path.exists(indicator_path):
                    return True
            
            # Check if it's a Documents/My Games directory
            if "Documents" in path and "My Games" in path:
                return True
                
            return False
            
        except Exception:
            return False
    
    def validate_current_path(self):
        """Validate the currently selected path"""
        current_path = self.poe2_path_var.get().strip()
        if not current_path:
            self.path_status_var.set("❌ ยังไม่ได้เลือกโฟลเดอร์")
            self.path_status_label.config(foreground="red")
            return
        
        if not os.path.exists(current_path):
            self.path_status_var.set("❌ โฟลเดอร์ไม่มีอยู่")
            self.path_status_label.config(foreground="red")
            return
        
        if self.validate_poe2_directory(current_path):
            self.path_status_var.set("✅ โฟลเดอร์นี้เหมาะสำหรับ POE2")
            self.path_status_label.config(foreground="green")
        else:
            self.path_status_var.set("⚠️  โฟลเดอร์นี้อาจไม่เหมาะสำหรับ POE2")
            self.path_status_label.config(foreground="orange")
    
    def update_path_status(self):
        """Update path status when path changes"""
        current_path = self.poe2_path_var.get().strip()
        if current_path:
            if os.path.exists(current_path):
                if self.validate_poe2_directory(current_path):
                    self.path_status_var.set("✅ โฟลเดอร์พร้อมใช้งาน")
                    self.path_status_label.config(foreground="green")
                else:
                    self.path_status_var.set("⚠️  โฟลเดอร์อาจไม่เหมาะ")
                    self.path_status_label.config(foreground="orange")
            else:
                self.path_status_var.set("❌ โฟลเดอร์ไม่มีอยู่")
                self.path_status_label.config(foreground="red")
        else:
            self.path_status_var.set("ยังไม่ได้เลือกโฟลเดอร์")
            self.path_status_label.config(foreground="orange")
    
    def auto_detect_poe2(self):
        """Auto-detect POE2 installation directory"""
        self.log_message("🔍 กำลังตรวจหาโฟลเดอร์ POE2...")
        
        poe2_path = self.installer.find_poe2_directory()
        if poe2_path:
            self.poe2_path_var.set(poe2_path)
            self.log_message(f"✅ พบโฟลเดอร์ POE2: {poe2_path}")
            
            # Check if it's a newly created directory
            if not os.path.exists(os.path.join(poe2_path, "User")):
                self.log_message("📁 สร้างโฟลเดอร์ใหม่สำหรับ POE2")
            else:
                self.log_message("📁 โฟลเดอร์ POE2 มีอยู่แล้ว")
        else:
            self.poe2_path_var.set("")
            self.log_message("❌ ไม่พบโฟลเดอร์ POE2 กรุณาเลือกเอง")
            self.log_message("💡 ลองใช้ปุ่ม 'เลือก' เพื่อเลือกโฟลเดอร์ หรือใช้ default paths")
        
        # Update status
        self.update_path_status()
    
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
    
    def check_installation_status(self):
        """Check and display installation status"""
        try:
            poe2_path = self.poe2_path_var.get().strip()
            if not poe2_path:
                return
            
            status = self.installer.filter_manager.get_installation_status(poe2_path)
            
            # Display status in log
            if status["essential_filters_installed"]:
                self.log_message(f"✅ Essential filters: {status['essential_filters_count']} files")
            else:
                self.log_message("❌ Essential filters not installed")
            
            if status["soundeffect_installed"]:
                size_mb = status["soundeffect_size"] / (1024 * 1024)
                self.log_message(f"✅ Sound effects: {size_mb:.1f} MB")
            else:
                self.log_message("❌ Sound effects not installed")
            
            if status["last_modified"]:
                self.log_message(f"📅 Last modified: {status['last_modified']}")
                
        except Exception as e:
            self.log_message(f"⚠️  ไม่สามารถตรวจสอบสถานะได้: {e}")
    
    def run(self):
        """Run the GUI"""
        try:
            self.root.mainloop()
        except Exception as e:
            self.logger.error(f"GUI error: {e}")
            messagebox.showerror("ข้อผิดพลาด", f"ข้อผิดพลาดใน GUI: {e}")
