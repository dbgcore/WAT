import tkinter as tk
from tkinter import ttk, messagebox
import platform
import re
import winreg
import os
import sys
import subprocess

class WindowsActivatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WAT")
        self.root.geometry("500x380")
        self.root.resizable(False, False)
        self.setup_ui()
        
    def setup_ui(self):
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.header = ttk.Label(self.main_frame, text="Windows Activation Tool", style='Header.TLabel')
        self.header.pack(pady=(0, 20))
        
        self.info_frame = ttk.Frame(self.main_frame)
        self.info_frame.pack(fill=tk.X, pady=5)
        
        self.version_label = ttk.Label(self.info_frame, text="Windows Version:")
        self.version_label.pack(side=tk.LEFT)
        
        self.version_value = ttk.Label(self.info_frame, text="")
        self.version_value.pack(side=tk.LEFT, padx=10)
        
        self.status_label = ttk.Label(self.info_frame, text="Status:")
        self.status_label.pack(side=tk.LEFT, padx=(20, 0))
        
        self.status_value = ttk.Label(self.info_frame, text="")
        self.status_value.pack(side=tk.LEFT, padx=10)
        
        self.key_frame = ttk.Frame(self.main_frame)
        self.key_frame.pack(fill=tk.X, pady=5)
        
        self.key_label = ttk.Label(self.key_frame, text="Product Key:")
        self.key_label.pack(side=tk.LEFT)
        
        self.key_value = ttk.Label(self.key_frame, text="", foreground="blue")
        self.key_value.pack(side=tk.LEFT, padx=10)
        
        self.progress = ttk.Progressbar(self.main_frame, orient=tk.HORIZONTAL, mode='determinate')
        self.progress.pack(fill=tk.X, pady=20)
        
        self.activate_btn = ttk.Button(self.main_frame, text="Activate", command=self.silent_activate)
        self.activate_btn.pack(pady=10)
        
        self.footer = ttk.Label(self.main_frame, text="tg: @onlycoop", foreground="gray")
        self.footer.pack(side=tk.BOTTOM, pady=10)
        
        self.check_status()
        
    def get_windows_version(self):
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion") as key:
                product_name = winreg.QueryValueEx(key, "ProductName")[0]
                return f"{product_name.split('[')[0].strip()}"
        except:
            return None
    
    def find_key_in_file(self, windows_version):
        try:
            with open('keys.txt', 'r', encoding='utf-8') as file:
                for line in file:
                    if windows_version.lower() in line.lower():
                        match = re.search(r'([A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5})', line)
                        if match:
                            return match.group(1)
        except:
            return None
    
    def is_windows_activated(self):
        try:
            result = subprocess.check_output('cscript //nologo slmgr.vbs /xpr', shell=True, stderr=subprocess.PIPE)
            return b"activated" in result.lower() or "активирована".encode('utf-8') in result.lower()
        except:
            return False
    
    def silent_activate(self):
        version = self.get_windows_version()
        key = self.find_key_in_file(version)
        
        if key:
            self.progress['value'] = 0
            try:
                subprocess.run(f'slmgr /ipk {key}', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
                self.progress['value'] = 50
                subprocess.run('slmgr /skms kms8.msguides.com', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
                self.progress['value'] = 80
                subprocess.run('slmgr /ato', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
                self.progress['value'] = 100
                self.check_status()
            except:
                pass
    
    def check_status(self):
        version = self.get_windows_version()
        if version:
            self.version_value.config(text=version)
            
            if self.is_windows_activated():
                self.status_value.config(text="Activated", foreground="green")
                self.activate_btn.config(state=tk.DISABLED)
            else:
                self.status_value.config(text="Not Activated", foreground="red")
                key = self.find_key_in_file(version)
                if key:
                    self.key_value.config(text=key)
                else:
                    self.key_value.config(text="Not Found", foreground="red")
                    self.activate_btn.config(state=tk.DISABLED)
        else:
            self.version_value.config(text="Detection Error")
            self.activate_btn.config(state=tk.DISABLED)

if __name__ == "__main__":
    if sys.platform != 'win32':
        print("This tool works only on Windows")
    else:
        root = tk.Tk()
        app = WindowsActivatorApp(root)
        root.mainloop()