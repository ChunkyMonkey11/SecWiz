"""
SecWiz - Professional Security Scanner
Main entry point for the application
"""

from gui.gui import SecWizGUI

def main():
    """Main entry point"""
    app = SecWizGUI()
    app.run()

if __name__ == "__main__":
    main()