import os
import bios
import constants

# --- CONFIGURATION ---
BASE_DIR = constants.BASE_DIR
STORAGE_NAME = constants.STORAGE_NAME
STORAGE_PATH = constants.STORAGE_PATH

def init_vfs():
    """Initializes the physical directory structure."""
    if not os.path.exists(STORAGE_PATH):
        try:
            os.makedirs(STORAGE_PATH)
            
            default_layout = {
                "autoexec.bat": "ECHO OFF\nVER",
                "config.sys": "FILES=30\nBUFFERS=20",
                "command.com": "Placeholder for command.com shell",
                "readme.txt": "Welcome to VS-DOS! This is an open-source DOS simulator, and right now you experiencing file system!\nYou can edit or add files via your OS file manager into the storage/ folder.",
                "dos": None,
                "dos/edit.com": "Placeholder for edit.com executable.",
                "dos/mouse.sys": "Placeholder for mouse.sys driver.",
                "dos/vsdos.sys": "Placeholder for msdos.sys library",
                "dos/io.sys": "Placeholder for io.sys library",
                "dos/commands.sys": "Placeholder for commands.sys library",
                "temp": None,
                "install": None,
                "install/setup.exe": "Placeholder for setup.exe installer.",
                "install/installer.log": "Initializing installer\nInitialized\nCopying files\nCopy complete\nInstallation successful",
                "install/vsdos.vaf": "Placeholder for VS-DOS installer archive file."
            }

            for path, content in default_layout.items():
                full_path = os.path.join(STORAGE_PATH, path)
                
                if content is None:
                    os.makedirs(full_path, exist_ok=True)
                else:
                    # Ensure parent directories exist
                    os.makedirs(os.path.dirname(full_path), exist_ok=True)
                    with open(full_path, "w") as f:
                        f.write(content)

            return f"Drive C: initialized in ./{STORAGE_NAME}/"
        except Exception as e:
            return f"Disk Error: Could not create storage directory. ({e})"
            
    return "Drive C: ready."

def get_vfs_metadata():
    """
    Calculates disk usage based on BIOS HDD size.
    Returns sizes in bytes.
    """
    # HDD size in MB from BIOS converted to Bytes
    total_capacity = bios.get_sys_info()["HDD"] * 1024 * 1024
    used_bytes = 0

    if os.path.exists(STORAGE_PATH):
        for root, dirs, files in os.walk(STORAGE_PATH):
            for name in files:
                fp = os.path.join(root, name)
                # Physical size on your real hard drive
                used_bytes += os.path.getsize(fp)

    return {
        "label": "VS-DOS_C",
        "total": total_capacity,
        "used": used_bytes,
        "free": max(0, total_capacity - used_bytes)
    }