#!/usr/bin/env python3
import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont

# Check for admin privileges on Windows
if sys.platform == "win32":
    import ctypes
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    if not is_admin():
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        except Exception as e:
            pass
        sys.exit()

class BatteryThresholdManagerWinApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Battery Threshold Manager")
        self.root.resizable(False, False)
        
        # Color Palette - Modern Premium Dark Mode
        self.colors = {
            "bg": "#1F2937",          # Dark Slate Grey
            "card_bg": "#111827",     # Deep Charcoal
            "text": "#F9FAFB",        # White/Slate-50
            "text_muted": "#9CA3AF",  # Muted Grey/Slate-400
            "btn_80": "#0D9488",      # Teal Accent
            "btn_80_hover": "#14B8A6",
            "btn_100": "#059669",     # Emerald Accent
            "btn_100_hover": "#10B981",
            "btn_refresh": "#4B5563",  # Cool Grey Accent
            "btn_refresh_hover": "#6B7280",
            "border": "#374151"       # Border Grey
        }
        
        self.root.configure(bg=self.colors["bg"])
        
        # Define Fonts
        self.title_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
        self.label_font = tkfont.Font(family="Helvetica", size=10, weight="normal")
        self.value_font = tkfont.Font(family="Helvetica", size=32, weight="bold")
        self.btn_font = tkfont.Font(family="Helvetica", size=11, weight="bold")
        self.status_font = tkfont.Font(family="Helvetica", size=9, slant="italic")

        # Detect manufacturer
        self.manufacturer = self.detect_manufacturer()
        self.supported_vendors = ["lenovo", "asus", "dell"]
        
        # Determine if current vendor is supported
        self.vendor_key = self.get_vendor_key()
        
        if self.vendor_key in self.supported_vendors:
            self.root.geometry("420x350")
            self.setup_ui()
            self.refresh_threshold()
        else:
            self.setup_unsupported_ui()

    def detect_manufacturer(self):
        if sys.platform != "win32":
            return "Generic Non-Windows Device"
        try:
            # Query manufacturer via PowerShell/WMI
            cmd = ["powershell", "-Command", "(Get-CimInstance -ClassName Win32_ComputerSystem).Manufacturer"]
            res = subprocess.run(cmd, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0)
            return res.stdout.strip()
        except Exception:
            return "Unknown"

    def get_vendor_key(self):
        m = self.manufacturer.lower()
        if "lenovo" in m:
            return "lenovo"
        elif "asus" in m:
            return "asus"
        elif "dell" in m:
            return "dell"
        return "unknown"

    def setup_unsupported_ui(self):
        self.root.geometry("450x385")
        
        # Top Header
        header_frame = tk.Frame(self.root, bg=self.colors["bg"], pady=15)
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            header_frame, 
            text="Battery Threshold Manager", 
            fg=self.colors["text"], 
            bg=self.colors["bg"],
            font=self.title_font
        )
        title_label.pack()
        
        # Error card
        error_card = tk.Frame(
            self.root, 
            bg=self.colors["card_bg"], 
            bd=1, 
            highlightbackground="#EF4444", 
            highlightthickness=1
        )
        error_card.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Warning icon/title
        warning_icon = tk.Label(
            error_card,
            text="⚠️",
            font=tkfont.Font(family="Helvetica", size=32),
            fg="#F59E0B",
            bg=self.colors["card_bg"]
        )
        warning_icon.pack(pady=(15, 5))
        
        warning_title = tk.Label(
            error_card,
            text="Hardware Not Supported",
            font=tkfont.Font(family="Helvetica", size=14, weight="bold"),
            fg="#EF4444",
            bg=self.colors["card_bg"]
        )
        warning_title.pack(pady=(0, 10))
        
        # Details message
        details_text = (
            f"Your laptop manufacturer '{self.manufacturer}' is not supported for automatic charge limiting via WMI.\n\n"
            "Currently supported Windows vendors: Lenovo, ASUS, and Dell.\n\n"
            "Please use your vendor's official companion application (e.g., Lenovo Vantage, MyASUS, Dell Power Manager) to configure limits."
        )
        
        details_label = tk.Label(
            error_card,
            text=details_text,
            font=self.label_font,
            fg=self.colors["text"],
            bg=self.colors["card_bg"],
            justify=tk.CENTER,
            wraplength=380
        )
        details_label.pack(padx=15, pady=5)
        
        # Close button
        btn_frame = tk.Frame(self.root, bg=self.colors["bg"])
        btn_frame.pack(fill=tk.X, padx=20, pady=(5, 15))
        
        btn_close = tk.Button(
            btn_frame,
            text="Close Application",
            font=self.btn_font,
            fg="#FFFFFF",
            bg=self.colors["btn_refresh"],
            activeforeground="#FFFFFF",
            activebackground=self.colors["btn_refresh_hover"],
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.root.destroy
        )
        btn_close.pack(fill=tk.X)
        btn_close.bind("<Enter>", lambda e: self.on_hover(btn_close, self.colors["btn_refresh_hover"]))
        btn_close.bind("<Leave>", lambda e: self.on_leave(btn_close, self.colors["btn_refresh"]))

    def setup_ui(self):
        # Top Header
        header_frame = tk.Frame(self.root, bg=self.colors["bg"], pady=15)
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            header_frame, 
            text="Battery Threshold Manager", 
            fg=self.colors["text"], 
            bg=self.colors["bg"],
            font=self.title_font
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text=f"Configure limits for {self.manufacturer}",
            fg=self.colors["text_muted"],
            bg=self.colors["bg"],
            font=self.label_font
        )
        subtitle_label.pack(pady=(2, 0))

        # Main Info Card Frame (Current Status Display)
        self.card = tk.Frame(
            self.root, 
            bg=self.colors["card_bg"], 
            bd=1, 
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )
        self.card.pack(fill=tk.X, padx=20, pady=10)
        
        info_label = tk.Label(
            self.card,
            text="CURRENT CHARGE LIMIT",
            fg=self.colors["text_muted"],
            bg=self.colors["card_bg"],
            font=self.label_font
        )
        info_label.pack(pady=(12, 0))
        
        self.value_label = tk.Label(
            self.card,
            text="--",
            fg=self.colors["text"],
            bg=self.colors["card_bg"],
            font=self.value_font
        )
        self.value_label.pack(pady=(5, 12))

        # Action Buttons Frame
        btn_frame = tk.Frame(self.root, bg=self.colors["bg"])
        btn_frame.pack(fill=tk.X, padx=20, pady=15)
        
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)
        
        self.btn_set_80 = tk.Button(
            btn_frame,
            text="Limit to 80%",
            font=self.btn_font,
            fg="#FFFFFF",
            bg=self.colors["btn_80"],
            activeforeground="#FFFFFF",
            activebackground=self.colors["btn_80_hover"],
            bd=0,
            padx=10,
            pady=8,
            cursor="hand2",
            command=lambda: self.set_threshold(80)
        )
        self.btn_set_80.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        self.btn_set_80.bind("<Enter>", lambda e: self.on_hover(self.btn_set_80, self.colors["btn_80_hover"]))
        self.btn_set_80.bind("<Leave>", lambda e: self.on_leave(self.btn_set_80, self.colors["btn_80"]))

        self.btn_set_100 = tk.Button(
            btn_frame,
            text="Limit to 100%",
            font=self.btn_font,
            fg="#FFFFFF",
            bg=self.colors["btn_100"],
            activeforeground="#FFFFFF",
            activebackground=self.colors["btn_100_hover"],
            bd=0,
            padx=10,
            pady=8,
            cursor="hand2",
            command=lambda: self.set_threshold(100)
        )
        self.btn_set_100.grid(row=0, column=1, padx=(5, 0), sticky="ew")
        self.btn_set_100.bind("<Enter>", lambda e: self.on_hover(self.btn_set_100, self.colors["btn_100_hover"]))
        self.btn_set_100.bind("<Leave>", lambda e: self.on_leave(self.btn_set_100, self.colors["btn_100"]))
        
        # Refresh and Secondary Actions
        action_subframe = tk.Frame(self.root, bg=self.colors["bg"])
        action_subframe.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        self.btn_refresh = tk.Button(
            action_subframe,
            text="↻ Refresh Status",
            font=self.label_font,
            fg=self.colors["text"],
            bg=self.colors["btn_refresh"],
            activeforeground=self.colors["text"],
            activebackground=self.colors["btn_refresh_hover"],
            bd=0,
            padx=10,
            pady=5,
            cursor="hand2",
            command=self.refresh_threshold
        )
        self.btn_refresh.pack(side=tk.RIGHT)
        self.btn_refresh.bind("<Enter>", lambda e: self.on_hover(self.btn_refresh, self.colors["btn_refresh_hover"]))
        self.btn_refresh.bind("<Leave>", lambda e: self.on_leave(self.btn_refresh, self.colors["btn_refresh"]))

        # Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            font=self.status_font,
            fg=self.colors["text_muted"],
            bg=self.colors["bg"],
            anchor="w",
            padx=10,
            pady=5
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def on_hover(self, button, hover_color):
        button.configure(bg=hover_color)

    def on_leave(self, button, normal_color):
        button.configure(bg=normal_color)

    def update_status(self, text):
        self.status_var.set(text)
        self.root.update_idletasks()

    def run_powershell(self, cmd_str):
        try:
            cmd = ["powershell", "-Command", cmd_str]
            res = subprocess.run(cmd, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0)
            return res.stdout.strip(), res.stderr.strip(), res.returncode
        except Exception as e:
            return "", str(e), -1

    def refresh_threshold(self):
        self.update_status("Reading current battery threshold...")
        
        if self.vendor_key == "lenovo":
            out, err, code = self.run_powershell("(Get-CimInstance -Namespace root/wmi -ClassName Lenovo_BatteryChargeLimit).ChargeLimit")
            if code == 0 and out.isdigit():
                self.value_label.configure(text=f"{out}%", fg=self.colors["text"])
                self.update_status(f"Currently configured limit: {out}%")
            else:
                self.value_label.configure(text="Error", fg="#EF4444")
                self.update_status("Error reading Lenovo WMI charge limit.")
                
        elif self.vendor_key == "dell":
            out, err, code = self.run_powershell("(Get-CimInstance -Namespace root/dcim/sysman -ClassName Dell_BIOSSetting | Where-Object Name -eq 'PrimaryBattUpperLimit').CurrentValue")
            if code == 0 and out.isdigit():
                self.value_label.configure(text=f"{out}%", fg=self.colors["text"])
                self.update_status(f"Currently configured limit: {out}%")
            else:
                self.value_label.configure(text="Error", fg="#EF4444")
                self.update_status("Error reading Dell WMI charge limit.")
                
        elif self.vendor_key == "asus":
            # ASUS limits are typically write-only via WMI.
            self.value_label.configure(text="Set-Only", fg="#F59E0B")
            self.update_status("ASUS charge limits are set-only (cannot read status).")

    def set_threshold(self, value):
        self.update_status(f"Setting battery charge threshold limit to {value}%...")
        
        success = False
        err_msg = ""
        
        if self.vendor_key == "lenovo":
            # Write threshold via WMI
            cmd_str = f"(Get-CimInstance -Namespace root/wmi -ClassName Lenovo_SetBatteryChargeThreshold).SetBatteryChargeThreshold({value})"
            out, err, code = self.run_powershell(cmd_str)
            if code == 0:
                success = True
            else:
                err_msg = err if err else "Lenovo WMI set failed."
                
        elif self.vendor_key == "asus":
            # ASUS uses control code 0x00120057 (1179735 in decimal)
            cmd_str = f"Invoke-CimMethod -Namespace root/wmi -ClassName ASUSAtkWmiInterface -MethodName ASUSWmiMethod -Arguments @{{Device_Dec = 1179735; Control_Dec = {value}}}"
            out, err, code = self.run_powershell(cmd_str)
            if code == 0:
                success = True
            else:
                err_msg = err if err else "ASUS WMI set failed."
                
        elif self.vendor_key == "dell":
            # First set configuration mode to Custom
            cmd_cfg = "Invoke-CimMethod -Namespace root/dcim/sysman -ClassName Dell_BIOSService -MethodName SetBIOSAttributes -Arguments @{AttributeName = 'PrimaryBattChargeCfg'; AttributeValue = 'Custom'}"
            out_cfg, err_cfg, code_cfg = self.run_powershell(cmd_cfg)
            
            # Then set limit
            cmd_lim = f"Invoke-CimMethod -Namespace root/dcim/sysman -ClassName Dell_BIOSService -MethodName SetBIOSAttributes -Arguments @{{AttributeName = 'PrimaryBattUpperLimit'; AttributeValue = '{value}'}}"
            out_lim, err_lim, code_lim = self.run_powershell(cmd_lim)
            
            if code_cfg == 0 and code_lim == 0:
                success = True
            else:
                err_msg = f"Config: {err_cfg}. Limit: {err_lim}."
                
        if success:
            self.update_status(f"Successfully updated threshold to {value}%!")
            messagebox.showinfo("Success", f"Battery threshold successfully set to {value}%.")
            self.refresh_threshold()
        else:
            self.update_status("Failed to apply threshold setting.")
            messagebox.showerror("Execution Error", f"Failed to set battery threshold:\n{err_msg}")
            self.refresh_threshold()

def main():
    root = tk.Tk()
    app = BatteryThresholdManagerWinApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
