"""
SecWiz GUI - Professional Security Scanner Interface

A modern CustomTkinter GUI with:
- Dark theme with navy accents
- Professional multi-panel layout
- Custom assets integration
- Modern security tool aesthetics

Author: Revant and Mansour
Version: 4.0
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
import threading
import os
from datetime import datetime
from PIL import Image, ImageTk
import json

# Configure CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Color scheme - removing green accents
COLORS = {
    "primary": "#2196F3",      # Blue instead of green
    "secondary": "#1976D2",     # Darker blue
    "accent": "#64B5F6",        # Light blue
    "success": "#4CAF50",       # Keep green only for success states
    "warning": "#FF9800",       # Orange for warnings
    "error": "#f44336",         # Red for errors
    "background": "#0a0a0a",    # Dark background
    "surface": "#1a1a2e",       # Surface color
    "surface_light": "#2d2d44", # Lighter surface
    "text": "#ffffff",          # White text
    "text_secondary": "#888888" # Secondary text
}

class SecWizGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("SecWiz - Professional Security Scanner")
        self.root.geometry("1400x900")
        self.root.configure(fg_color="#0a0a0a")
        
        # Variables
        self.scan_type = tk.StringVar(value="full")
        self.target_domain = tk.StringVar()
        self.scan_running = False
        self.scan_results = {}
        
        # Tab configurations for different scan types
        self.tab_configs = {
            "full": ["overview", "ports", "directories", "vulnerabilities", "logs"],
            "port": ["all_ports", "open_ports_services", "logs"],
            "directory": ["all_files", "accessible_files", "protected_files", "logs"]
        }
        
        self.tab_names = {
            "full": {
                "overview": "Overview",
                "ports": "Ports", 
                "directories": "Directories",
                "vulnerabilities": "Vulns",
                "logs": "Logs"
            },
            "port": {
                "all_ports": "All Ports",
                "open_ports_services": "Open Ports & Services", 
                "logs": "Logs"
            },
            "directory": {
                "all_files": "All Files",
                "accessible_files": "Accessible Files",
                "protected_files": "Protected Files",
                "logs": "Logs"
            }
        }
        
        # Load assets
        self.load_assets()
        
        # Setup UI
        self.setup_ui()
        
    def load_assets(self):
        """Load and prepare assets"""
        try:
            # Load logo
            logo_path = os.path.join("assets", "SecWiz Logo.webp")
            if os.path.exists(logo_path):
                self.logo_image = ctk.CTkImage(
                    light_image=Image.open(logo_path),
                    dark_image=Image.open(logo_path),
                    size=(40, 40)
                )
            else:
                self.logo_image = None
                
            # Load button images
            self.button_images = {}
            button_assets = {
                "full": "button_full-scan.png",
                "port": "button_port-scan .png",
                "directory": "button_directory-scan.png"
            }
            
            for key, filename in button_assets.items():
                asset_path = os.path.join("assets", filename)
                if os.path.exists(asset_path):
                    self.button_images[key] = ctk.CTkImage(
                        light_image=Image.open(asset_path),
                        dark_image=Image.open(asset_path),
                        size=(200, 60)
                    )
                else:
                    self.button_images[key] = None
                    
        except Exception as e:
            print(f"Error loading assets: {e}")
            self.logo_image = None
            self.button_images = {}
        
    def setup_ui(self):
        """Setup the main UI"""
        # Main container
        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        self.setup_header()
        
        # Content area
        content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, pady=(20, 0))
        
        # Left panel (Scan Configuration)
        self.setup_scan_panel(content_frame)
        
        # Right panel (Results)
        self.setup_results_panel(content_frame)
        
    def setup_header(self):
        """Setup the header with logo and branding"""
        header_frame = ctk.CTkFrame(self.main_frame, fg_color=COLORS["surface"], height=80)
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Logo and title
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(side="left", padx=20, pady=20)
        
        if self.logo_image:
            logo_label = ctk.CTkLabel(title_frame, image=self.logo_image, text="")
            logo_label.pack(side="left", padx=(0, 15))
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="SecWiz",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=COLORS["primary"]
        )
        title_label.pack(side="left", padx=(0, 10))
        
        subtitle_label = ctk.CTkLabel(
            title_frame,
            text="Professional Security Scanner",
            font=ctk.CTkFont(size=14),
            text_color=COLORS["text_secondary"]
        )
        subtitle_label.pack(side="left")
        
        # Toolbar buttons
        toolbar_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        toolbar_frame.pack(side="right", padx=20, pady=20)
        
        # File button
        file_btn = ctk.CTkButton(
            toolbar_frame,
            text="📁 File",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=COLORS["surface_light"],
            hover_color=COLORS["primary"],
            width=80,
            height=32,
            command=self.show_file_menu
        )
        file_btn.pack(side="left", padx=(0, 10))
        
        # Tools button
        tools_btn = ctk.CTkButton(
            toolbar_frame,
            text="🔧 Tools",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=COLORS["surface_light"],
            hover_color=COLORS["primary"],
            width=80,
            height=32,
            command=self.show_tools_menu
        )
        tools_btn.pack(side="left", padx=(0, 10))
        
        # Help button
        help_btn = ctk.CTkButton(
            toolbar_frame,
            text="❓ Help",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=COLORS["surface_light"],
            hover_color=COLORS["primary"],
            width=80,
            height=32,
            command=self.show_help_menu
        )
        help_btn.pack(side="left")
        
    def setup_scan_panel(self, parent):
        """Setup the scan configuration panel"""
        # Left panel container
        scan_frame = ctk.CTkFrame(parent, fg_color=COLORS["surface"], width=400)
        scan_frame.pack(side="left", fill="y", padx=(0, 20))
        scan_frame.pack_propagate(False)
        
        # Panel header
        header_label = ctk.CTkLabel(
            scan_frame,
            text="🔍 Scan Configuration",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS["text"]
        )
        header_label.pack(pady=(20, 30))
        
        # Scan type selection
        scan_type_frame = ctk.CTkFrame(scan_frame, fg_color="transparent")
        scan_type_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        scan_type_label = ctk.CTkLabel(
            scan_type_frame,
            text="Select Scan Type:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS["text"]
        )
        scan_type_label.pack(anchor="w", pady=(0, 15))
        
        # Scan type buttons
        self.scan_buttons = {}
        scan_types = [
            ("full", "Full Scan", "Complete vulnerability assessment"),
            ("port", "Port Scan", "Port and service enumeration"),
            ("directory", "Directory Scan", "Directory enumeration")
        ]
        
        for scan_type, title, desc in scan_types:
            # Create button frame
            button_frame = ctk.CTkFrame(scan_type_frame, fg_color="transparent")
            button_frame.pack(fill="x", pady=(0, 10))
            
            # Use custom image if available
            if scan_type in self.button_images and self.button_images[scan_type]:
                btn = ctk.CTkButton(
                    button_frame,
                    text="",
                    image=self.button_images[scan_type],
                    fg_color="transparent",
                    hover_color=COLORS["primary"],
                    width=200,
                    height=60,
                    command=lambda t=scan_type: self.select_scan_type(t)
                )
            else:
                # Fallback to text button
                btn = ctk.CTkButton(
                    button_frame,
                    text=title,
                    font=ctk.CTkFont(size=12, weight="bold"),
                    fg_color=COLORS["surface_light"],
                    hover_color=COLORS["primary"],
                    width=200,
                    height=60,
                    command=lambda t=scan_type: self.select_scan_type(t)
                )
            
            btn.pack(side="left")
            self.scan_buttons[scan_type] = btn
            
            # Description label
            desc_label = ctk.CTkLabel(
                button_frame,
                text=desc,
                font=ctk.CTkFont(size=10),
                text_color=COLORS["text_secondary"]
            )
            desc_label.pack(side="left", padx=(10, 0))
        
        # Target configuration
        target_frame = ctk.CTkFrame(scan_frame, fg_color="transparent")
        target_frame.pack(fill="x", padx=20, pady=(20, 0))
        
        target_label = ctk.CTkLabel(
            target_frame,
            text="Target Configuration:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS["text"]
        )
        target_label.pack(anchor="w", pady=(0, 10))
        
        # Target input
        self.target_entry = ctk.CTkEntry(
            target_frame,
            placeholder_text="Enter target domain (e.g., testphp.vulnweb.com)",
            font=ctk.CTkFont(size=12),
            height=40,
            fg_color=COLORS["surface_light"],
            border_color=COLORS["primary"],
            text_color=COLORS["text"]
        )
        self.target_entry.pack(fill="x", pady=(0, 10))
        
        # Example label
        example_label = ctk.CTkLabel(
            target_frame,
            text="💡 Example: testphp.vulnweb.com",
            font=ctk.CTkFont(size=10),
            text_color=COLORS["text_secondary"]
        )
        example_label.pack(anchor="w")
        
        # Action buttons
        action_frame = ctk.CTkFrame(scan_frame, fg_color="transparent")
        action_frame.pack(fill="x", padx=20, pady=30)
        
        # Start button
        self.start_btn = ctk.CTkButton(
            action_frame,
            text="🚀 Start Scan",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=COLORS["primary"],
            hover_color=COLORS["secondary"],
            height=45,
            command=self.start_scan
        )
        self.start_btn.pack(fill="x", pady=(0, 10))
        
        # Stop button
        self.stop_btn = ctk.CTkButton(
            action_frame,
            text="⏹️ Stop Scan",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=COLORS["error"],
            hover_color="#d32f2f",
            height=45,
            command=self.stop_scan,
            state="disabled"
        )
        self.stop_btn.pack(fill="x", pady=(0, 10))
        
        # Results button
        self.results_btn = ctk.CTkButton(
            action_frame,
            text="📊 View Results",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=COLORS["accent"],
            hover_color=COLORS["secondary"],
            height=45,
            command=self.view_results,
            state="disabled"
        )
        self.results_btn.pack(fill="x", pady=(0, 10))
        
        # Report button
        self.report_btn = ctk.CTkButton(
            action_frame,
            text="📄 Generate Report",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=COLORS["warning"],
            hover_color="#F57C00",
            height=45,
            command=self.generate_report,
            state="disabled"
        )
        self.report_btn.pack(fill="x")
        
        # Status
        status_frame = ctk.CTkFrame(scan_frame, fg_color="transparent")
        status_frame.pack(fill="x", padx=20, pady=20)
        
        self.status_var = tk.StringVar(value="✅ Ready to scan")
        self.status_label = ctk.CTkLabel(
            status_frame,
            textvariable=self.status_var,
            font=ctk.CTkFont(size=12),
            text_color=COLORS["success"]
        )
        self.status_label.pack(anchor="w")
        
        # Initialize scan type (tabs will be set up later)
        self.scan_type.set("full")
        
        # Update button states
        for key, btn in self.scan_buttons.items():
            if key == "full":
                btn.configure(fg_color=COLORS["primary"], hover_color=COLORS["secondary"])
            else:
                btn.configure(fg_color=COLORS["surface_light"], hover_color=COLORS["primary"])
        
    def setup_results_panel(self, parent):
        """Setup the results panel"""
        # Right panel container
        results_frame = ctk.CTkFrame(parent, fg_color=COLORS["surface"])
        results_frame.pack(side="right", fill="both", expand=True)
        
        # Panel header
        header_label = ctk.CTkLabel(
            results_frame,
            text="📊 Scan Results",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS["text"]
        )
        header_label.pack(pady=(20, 30))
        
        # Tab container
        self.tab_container = ctk.CTkFrame(results_frame, fg_color="transparent")
        self.tab_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Tab buttons
        self.tab_buttons_frame = ctk.CTkFrame(self.tab_container, fg_color="transparent")
        self.tab_buttons_frame.pack(fill="x", pady=(0, 15))
        
        self.tab_buttons = {}
        
        # Initialize with default tabs for full scan
        self.update_tabs_for_scan_type("full")
        
        # Tab content
        self.tab_content = ctk.CTkFrame(self.tab_container, fg_color=COLORS["surface_light"])
        self.tab_content.pack(fill="both", expand=True)
        
        # Content text area
        self.content_text = ctk.CTkTextbox(
            self.tab_content,
            font=ctk.CTkFont(size=11, family="Consolas"),
            fg_color=COLORS["surface_light"],
            text_color=COLORS["success"],
            wrap="word"
        )
        self.content_text.pack(fill="both", expand=True, padx=15, pady=15)
        
    def select_scan_type(self, scan_type):
        """Select scan type"""
        self.scan_type.set(scan_type)
        
        # Update button states
        for key, btn in self.scan_buttons.items():
            if key == scan_type:
                btn.configure(fg_color=COLORS["primary"], hover_color=COLORS["secondary"])
            else:
                btn.configure(fg_color=COLORS["surface_light"], hover_color=COLORS["primary"])
        
                # Update tabs based on scan type
        self.update_tabs_for_scan_type(scan_type)
        
    def update_tabs_for_scan_type(self, scan_type):
        """Update tabs based on selected scan type"""
        # Check if tab_buttons exists (might not be initialized yet)
        if not hasattr(self, 'tab_buttons'):
            return
            
        # Clear existing tab buttons
        for btn in self.tab_buttons.values():
            btn.destroy()
        self.tab_buttons.clear()
        
        # Get tabs for this scan type
        tab_ids = self.tab_configs.get(scan_type, [])
        tab_names = self.tab_names.get(scan_type, {})
        
        # Create new tab buttons
        for tab_id in tab_ids:
            tab_name = tab_names.get(tab_id, tab_id.title())
            btn = ctk.CTkButton(
                self.tab_buttons_frame,
                text=tab_name,
                font=ctk.CTkFont(size=12, weight="bold"),
                fg_color=COLORS["surface_light"],
                hover_color=COLORS["primary"],
                width=120,
                height=35,
                command=lambda t=tab_id: self.show_tab(t)
            )
            btn.pack(side="left", padx=(0, 10))
            self.tab_buttons[tab_id] = btn
        
        # Show first tab
        if tab_ids:
            self.show_tab(tab_ids[0])
        
    def start_scan(self):
        """Start scan"""
        target = self.target_entry.get().strip()
        
        if not target:
            messagebox.showerror("Error", "Please enter a target domain")
            return
            
        if self.scan_running:
            messagebox.showwarning("Warning", "Scan already in progress")
            return
            
        self.scan_running = True
        self.update_status("🔄 Scanning in progress...", COLORS["warning"])
        
        # Update button states
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.results_btn.configure(state="disabled")
        self.report_btn.configure(state="disabled")
        
        # Start scan thread
        scan_thread = threading.Thread(target=self.run_scan, args=(target,))
        scan_thread.daemon = True
        scan_thread.start()
        
    def run_scan(self, target):
        """Run the scan"""
        try:
            scan_type = self.scan_type.get()
            
            if scan_type == "full":
                self.run_full_scan(target)
            elif scan_type == "port":
                self.run_port_scan(target)
            elif scan_type == "directory":
                self.run_gobuster_scan(target)
        except Exception as e:
            self.update_status(f"❌ Error: {str(e)}", COLORS["error"])
        finally:
            self.scan_complete()
            
    def run_full_scan(self, target):
        """Run full scan"""
        self.update_status("🔍 Step 1/4: Port Scanning...", COLORS["warning"])
        # TODO: Call your port scanner
        # from tools.portScanner import scan_ports
        # scan_ports(target)
        
        self.update_status("📁 Step 2/4: Directory Enumeration...", COLORS["warning"])
        # TODO: Call your gobuster scanner
        # from tools.gobuster_scan import run_gobuster_scan
        # run_gobuster_scan([f"http://{target}"])
        
        self.update_status("📝 Step 3/4: Form Input Extraction...", COLORS["warning"])
        # TODO: Call your parameter scanner
        # from tools.parmScanner import fetch_forms_inputs
        # forms = fetch_forms_inputs(f"http://{target}/login.php")
        
        self.update_status("🗄️ Step 4/4: SQL Injection Testing...", COLORS["warning"])
        # TODO: Call your SQL scanner
        # from tools.sqlScanner import sqlScanner
        # sqlScanner([f"http://{target}/login.php"])
        
        # Store results
        self.scan_results = {
            'type': 'full',
            'target': target,
            'timestamp': datetime.now().isoformat(),
            'results': f"Full scan completed for {target}"
        }
        
        self.update_status("✅ Full scan completed successfully!", COLORS["success"])
        
    def run_port_scan(self, target):
        """Run port scan"""
        self.update_status("🔍 Port scanning in progress...", COLORS["warning"])
        
        # TODO: Call your port scanner
        # from tools.portScanner import scan_ports
        # scan_ports(target)
        
        self.scan_results = {
            'type': 'port',
            'target': target,
            'timestamp': datetime.now().isoformat(),
            'results': f"Port scan completed for {target}"
        }
        
        self.update_status("✅ Port scan completed successfully!", COLORS["success"])
        
    def run_gobuster_scan(self, target):
        """Run gobuster scan"""
        self.update_status("📁 Directory scanning in progress...", COLORS["warning"])
        
        # TODO: Call your gobuster scanner
        # from tools.gobuster_scan import run_gobuster_scan
        # run_gobuster_scan([f"http://{target}"])
        
        self.scan_results = {
            'type': 'gobuster',
            'target': target,
            'timestamp': datetime.now().isoformat(),
            'results': f"Directory scan completed for {target}"
        }
        
        self.update_status("✅ Directory scan completed successfully!", COLORS["success"])
        
    def stop_scan(self):
        """Stop scan"""
        self.scan_running = False
        self.update_status("⏹️ Scan stopped by user", COLORS["error"])
        self.scan_complete()
        
    def scan_complete(self):
        """Handle scan completion"""
        self.scan_running = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.results_btn.configure(state="normal")
        self.report_btn.configure(state="normal")
        
    def update_status(self, message, color=COLORS["success"]):
        """Update status"""
        self.status_var.set(message)
        self.status_label.configure(text_color=color)
        
    def show_tab(self, tab_id):
        """Show specific tab content"""
        # Check if tab_buttons exists
        if not hasattr(self, 'tab_buttons'):
            return
            
        # Update button states
        for key, btn in self.tab_buttons.items():
            if key == tab_id:
                btn.configure(fg_color=COLORS["primary"], hover_color=COLORS["secondary"])
            else:
                btn.configure(fg_color=COLORS["surface_light"], hover_color=COLORS["primary"])
                
        # Update content
        if hasattr(self, 'content_text'):
            self.content_text.delete("0.0", "end")
            
            # Get current scan type
            scan_type = self.scan_type.get()
            
            # Content based on scan type and tab
            content = self.get_tab_content(scan_type, tab_id)
            
            self.content_text.insert("0.0", content)
        
    def get_tab_content(self, scan_type, tab_id):
        """Get content for specific tab based on scan type"""
        if scan_type == "full":
            content_map = {
                "overview": "Full Scan Overview\n\nComplete vulnerability assessment results will be displayed here.",
                "ports": "Port Scan Results\n\nOpen ports and services will be listed here.",
                "directories": "Directory Enumeration Results\n\nDiscovered directories and files will be shown here.",
                "vulnerabilities": "Vulnerability Assessment Results\n\nIdentified security vulnerabilities will be displayed here.",
                "logs": "Full Scan Logs\n\nDetailed scan logs and execution history."
            }
        elif scan_type == "port":
            content_map = {
                "all_ports": "All Ports Scan Results\n\nComplete port scan results including open and closed ports.",
                "open_ports_services": "Open Ports & Services Results\n\nOpen ports with their running services and applications detected.",
                "logs": "Port Scan Logs\n\nDetailed port scanning logs and execution history."
            }
        elif scan_type == "directory":
            content_map = {
                "all_files": "All Files Discovered\n\nComplete list of all files and directories found.",
                "accessible_files": "Accessible Files\n\nFiles that are publicly accessible and readable.",
                "protected_files": "Protected Files\n\nFiles that require authentication or are restricted.",
                "logs": "Directory Scan Logs\n\nDetailed directory enumeration logs and execution history."
            }
        else:
            content_map = {
                "overview": "Scan Overview\n\nNo scan results available yet.",
                "logs": "Scan Logs\n\nNo scan logs available yet."
            }
        
        return content_map.get(tab_id, f"Content for {tab_id} not available")
        
    def view_results(self):
        """View results"""
        if not self.scan_results:
            messagebox.showinfo("Info", "No scan results available")
            return
            
        # Create results window
        results_window = ctk.CTkToplevel(self.root)
        results_window.title("SecWiz Scan Results")
        results_window.geometry("800x600")
        results_window.configure(fg_color=COLORS["surface"])
        
        # Results content
        results_text = ctk.CTkTextbox(
            results_window,
            font=ctk.CTkFont(size=11, family="Consolas"),
            fg_color=COLORS["surface_light"],
            text_color=COLORS["success"]
        )
        results_text.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Display results
        results_content = f"""
╔══════════════════════════════════════════════════════════════╗
║                    SECWIZ SCAN RESULTS                       ║
╚══════════════════════════════════════════════════════════════╝

Scan Information:
• Scan Type: {self.scan_results.get('type', 'Unknown').upper()} SCAN
• Target: {self.scan_results.get('target', 'Unknown')}
• Date: {self.scan_results.get('timestamp', 'Unknown')}
• Status: COMPLETED

{'='*60}

SCAN RESULTS:
{self.scan_results.get('results', 'No results available')}

{'='*60}

Report generated by SecWiz Security Scanner
Developed by Revant and Mansour
        """
        
        results_text.insert("0.0", results_content)
        
    def generate_report(self):
        """Generate report"""
        if not self.scan_results:
            messagebox.showinfo("Info", "No scan results to report")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Scan Report"
        )
        
        if filename:
            try:
                report_content = f"""
╔══════════════════════════════════════════════════════════════╗
║                    SECWIZ SCAN REPORT                        ║
╚══════════════════════════════════════════════════════════════╝

Scan Information:
• Scan Type: {self.scan_results.get('type', 'Unknown').upper()} SCAN
• Target: {self.scan_results.get('target', 'Unknown')}
• Date: {self.scan_results.get('timestamp', 'Unknown')}
• Status: COMPLETED

{'='*60}

SCAN RESULTS:
{self.scan_results.get('results', 'No results available')}

{'='*60}

Report generated by SecWiz Security Scanner
Developed by Revant and Mansour
                """
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(report_content)
                messagebox.showinfo("Success", f"Report saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save report: {str(e)}")
                
    def show_file_menu(self):
        """Show file menu"""
        messagebox.showinfo("File Menu", "File menu functionality coming soon!")
        
    def show_tools_menu(self):
        """Show tools menu"""
        messagebox.showinfo("Tools Menu", "Tools menu functionality coming soon!")
        
    def show_help_menu(self):
        """Show help menu"""
        messagebox.showinfo("Help Menu", "Help menu functionality coming soon!")
        
    def run(self):
        """Run the application"""
        self.root.mainloop()

def main():
    """Main entry point"""
    app = SecWizGUI()
    app.run()

if __name__ == "__main__":
    main() 