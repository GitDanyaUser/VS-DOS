import sys
import os
import subprocess

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def main():
    print("--- VS-DOS Boot Menu ---")
    print("1. Boot VS-DOS (main.py)")
    print("2. Launch GUI Test (gui_colorful_test.py)")
    print("3. Exit")
    
    choice = input("\nSelection: ")

    # We use resource_path to find the bundled scripts
    if choice == '1':
        script = resource_path("main.py")
        subprocess.run([sys.executable, script])
    elif choice == '2':
        script = resource_path("gui_colorful_test.py")
        subprocess.run([sys.executable, script])
    elif choice == '3':
        sys.exit()

if __name__ == "__main__":
    main()