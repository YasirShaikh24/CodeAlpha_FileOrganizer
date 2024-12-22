import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import shutil
import psutil # type: ignore
import tempfile
import subprocess
import platform
import time
from datetime import datetime, timedelta

class SystemMaintenanceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("System Maintenance & File Organizer")
        self.root.geometry("800x600")
        self.system = platform.system()
        
        # Configure the dark theme
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Define colors
        self.bg_color = "#2b2b2b"
        self.fg_color = "#ffffff"
        self.button_bg = "#404040"
        self.button_fg = "#ffffff"
        self.frame_bg = "#333333"
        
        # Configure styles
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TButton', 
                           font=('Times New Roman', 11),
                           background=self.button_bg,
                           foreground=self.button_fg,
                           padding=5)
        self.style.configure('TLabel',
                           font=('Times New Roman', 11),
                           background=self.bg_color,
                           foreground=self.fg_color)
        self.style.configure('Header.TLabel',
                           font=('Times New Roman', 16, 'bold'),
                           background=self.bg_color,
                           foreground=self.fg_color)
        
        # Configure root window
        self.root.configure(bg=self.bg_color)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Header
        header_label = ttk.Label(main_frame,
                               text="System Maintenance & File Organizer",
                               style='Header.TLabel')
        header_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Buttons Frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=1, column=0, sticky="nsew", padx=10)
        
        # Status Frame
        self.status_frame = ttk.Frame(main_frame)
        self.status_frame.grid(row=1, column=1, sticky="nsew", padx=10)
        
        # Status Text
        self.status_text = tk.Text(self.status_frame,
                                 wrap=tk.WORD,
                                 width=40,
                                 height=20,
                                 font=('Times New Roman', 11),
                                 bg=self.frame_bg,
                                 fg=self.fg_color)
        self.status_text.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbar for status text
        scrollbar = ttk.Scrollbar(self.status_frame,
                                orient="vertical",
                                command=self.status_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        # Create main buttons
        buttons = [
            ("File Organization", self.file_organization),
            ("Disk Cleanup", self.disk_cleanup),
            ("System Performance", self.system_performance_check),
            ("Temporary Files Cleanup", self.temporary_files_cleanup),
            ("Unnecessary Files Removal", self.unnecessary_files_removal),
            ("System Information", self.display_system_info)
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(buttons_frame, text=text, command=command)
            btn.grid(row=i, column=0, pady=5, sticky="ew")
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        self.status_frame.grid_columnconfigure(0, weight=1)
        self.status_frame.grid_rowconfigure(0, weight=1)
        
    def update_status(self, message):
        """Update the status text widget with a new message."""
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(tk.END, message)
        
    def file_organization(self):
        """File organization functionality with GUI."""
        directory = filedialog.askdirectory(title="Select Directory to Organize")
        if not directory:
            return
            
        FILE_CATEGORIES = {
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
            "Documents": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx"],
            "Videos": [".mp4", ".mkv", ".avi", ".mov", ".flv"],
            "Audio": [".mp3", ".wav", ".aac", ".flac"],
            "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
            "Code": [".py", ".java", ".cpp", ".js", ".html", ".css"],
            "Others": []
        }
        
        try:
            status_message = "Organizing files...\n\n"
            
            # Create category folders
            for category in FILE_CATEGORIES:
                category_path = os.path.join(directory, category)
                os.makedirs(category_path, exist_ok=True)
            
            # Organize files
            for file in os.listdir(directory):
                file_path = os.path.join(directory, file)
                if os.path.isdir(file_path):
                    continue
                
                _, file_extension = os.path.splitext(file)
                moved = False
                
                for category, extensions in FILE_CATEGORIES.items():
                    if file_extension.lower() in extensions:
                        shutil.move(file_path, os.path.join(directory, category, file))
                        status_message += f"Moved {file} to {category}\n"
                        moved = True
                        break
                
                if not moved:
                    shutil.move(file_path, os.path.join(directory, "Others", file))
                    status_message += f"Moved {file} to Others\n"
                
            status_message += "\nFile organization completed successfully!"
            self.update_status(status_message)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            
    def disk_cleanup(self):
        """Perform disk cleanup with GUI feedback."""
        try:
            status_message = "Performing disk cleanup...\n\n"
            
            if self.system == "Windows":
                subprocess.run(["cleanmgr"], shell=True)
                status_message += "Windows Disk Cleanup utility launched.\n"
            elif self.system == "Darwin":
                subprocess.run(["sudo", "rm", "-rf", "~/.Trash/*"])
                subprocess.run(["sudo", "rm", "-rf", "/private/var/log/*"])
                status_message += "macOS cleanup completed.\n"
            elif self.system == "Linux":
                subprocess.run(["sudo", "apt", "clean"])
                subprocess.run(["sudo", "journalctl", "--vacuum-time=3d"])
                status_message += "Linux cleanup completed.\n"
                
            status_message += "\nDisk cleanup completed successfully!"
            self.update_status(status_message)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            
    def system_performance_check(self):
        """Check system performance with GUI display."""
        try:
            status_message = "System Performance Report\n"
            status_message += "=" * 30 + "\n\n"
            
            # CPU Usage
            status_message += f"CPU Usage: {psutil.cpu_percent()}%\n\n"
            
            # Memory Usage
            memory = psutil.virtual_memory()
            status_message += "Memory Usage:\n"
            status_message += f"Total: {memory.total / (1024**3):.2f} GB\n"
            status_message += f"Available: {memory.available / (1024**3):.2f} GB\n"
            status_message += f"Used: {memory.percent}%\n\n"
            
            # Disk Usage
            disk = psutil.disk_usage('/')
            status_message += "Disk Usage:\n"
            status_message += f"Total: {disk.total / (1024**3):.2f} GB\n"
            status_message += f"Free: {disk.free / (1024**3):.2f} GB\n"
            status_message += f"Used: {disk.percent}%"
            
            self.update_status(status_message)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            
    def temporary_files_cleanup(self):
        """Clean temporary files with GUI feedback."""
        try:
            status_message = "Cleaning temporary files...\n\n"
            temp_dir = tempfile.gettempdir()
            current_time = time.time()
            files_removed = 0
            
            for filename in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, filename)
                try:
                    if os.path.isfile(file_path):
                        file_modified = os.path.getmtime(file_path)
                        if current_time - file_modified > 7 * 86400:
                            os.unlink(file_path)
                            status_message += f"Removed: {filename}\n"
                            files_removed += 1
                except Exception as e:
                    status_message += f"Error removing {filename}: {str(e)}\n"
                    
            status_message += f"\nCleanup completed. Removed {files_removed} files."
            self.update_status(status_message)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            
    def unnecessary_files_removal(self):
        """Remove unnecessary files with GUI feedback."""
        try:
            status_message = "Removing unnecessary files...\n\n"
            
            if self.system == "Windows":
                status_message += "Windows cleanup:\n"
                subprocess.run(["net", "stop", "wuauserv"], shell=True)
                subprocess.run(["rmdir", "/S", "/Q", r"C:\Windows\SoftwareDistribution"], shell=True)
                subprocess.run(["net", "start", "wuauserv"], shell=True)
                status_message += "- Cleared Windows Update cache\n"
            elif self.system == "Darwin":
                status_message += "macOS cleanup:\n"
                subprocess.run(["rm", "-rf", "~/Library/Caches/*"])
                subprocess.run(["rm", "-rf", "~/Library/Logs/*"])
                status_message += "- Cleared system caches and logs\n"
            elif self.system == "Linux":
                status_message += "Linux cleanup:\n"
                subprocess.run(["sudo", "apt", "autoremove"], check=True)
                subprocess.run(["sudo", "apt", "autoclean"], check=True)
                status_message += "- Removed unused packages\n"
                
            status_message += "\nUnnecessary files removal completed!"
            self.update_status(status_message)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            
    def display_system_info(self):
        """Display system information in GUI."""
        try:
            status_message = "System Information\n"
            status_message += "=" * 30 + "\n\n"
            
            status_message += f"Operating System: {platform.system()} {platform.release()}\n"
            status_message += f"Machine: {platform.machine()}\n"
            status_message += f"Processor: {platform.processor()}\n"
            status_message += f"Python Version: {platform.python_version()}\n\n"
            
            # Network Information
            try:
                import socket
                hostname = socket.gethostname()
                ip_address = socket.gethostbyname(hostname)
                status_message += "Network Information:\n"
                status_message += f"Hostname: {hostname}\n"
                status_message += f"IP Address: {ip_address}\n"
            except Exception as e:
                status_message += f"Network Info Error: {str(e)}\n"
                
            self.update_status(status_message)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    root = tk.Tk()
    app = SystemMaintenanceGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()