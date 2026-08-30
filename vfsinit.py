import os
import bios
from utils import gen_rand_bytes
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
                # Boot / startup files
                "autoexec.bat": "ECHO OFF\nVER\n",
                "config.sys": "FILES=30\nBUFFERS=20\n",

                # DOS-like system binaries
                "command.com": gen_rand_bytes(96769),
                "dos/mouse.sys": gen_rand_bytes(21312),
                "dos/vsdos.sys": gen_rand_bytes(65536),
                "dos/io.sys": gen_rand_bytes(40960),
                "dos/commands.sys": gen_rand_bytes(131072),

                # Text files
                "readme.txt":
                    "Welcome to VS-DOS! This is an open-source DOS simulator, "
                    "and right now you are experiencing the file system!\n"
                    "You can edit or add files via your OS file manager into "
                    "the storage/ folder.\n",

                # Directories
                "dos": None,
                "temp": None,
                "install": None,

                # DOS programs / binaries
                "dos/edit.com": gen_rand_bytes(68124),

                # Installer files
                "install/setup.exe": gen_rand_bytes(524288),

                "install/installer.log":
                    "Initializing installer\n"
                    "Initialized\n"
                    "Copying files\n"
                    "Copy complete\n"
                    "Installation successful\n",

                # VS-DOS archive
                "install/vsdos.vaf": gen_rand_bytes(1572864),
            }

            for path, content in default_layout.items():
                full_path = os.path.join(STORAGE_PATH, path)
                
                if content is None:
                    os.makedirs(full_path, exist_ok=True)
                else:
                    # Ensure parent directories exist
                    os.makedirs(os.path.dirname(full_path), exist_ok=True)
                    
                    # Handle bytes vs string writing modes
                    if isinstance(content, bytes):
                        with open(full_path, "wb") as f:
                            f.write(content)
                    else:
                        with open(full_path, "w", encoding="utf-8") as f:
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