import json
import os

VFS_PATH = "fonts/filestorage.json"

def init_vfs():
    """Creates the disk if it doesn't exist."""
    if not os.path.exists(VFS_PATH):
        empty_vfs = {
            "metadata": {
                "label": "VS-DOS_C",
                "total_size_bytes": __import__("bios").get_sys_info()["HDD"] * 1024 * 1024,
                "used_size_bytes": 0
            },
            "files": {
                "autoexec.bat": "ECHO OFF\nVER",
                "config.sys": "FILES=30\nBUFFERS=20",
                "readme.txt": "Welcome to VS-DOS Beta 2!\nThis is a virtual disk drive C: used for testing file operations.\nFeel free to modify or add files here."
            },
            "folders": {
                "dos": {
                    "files": {
                        "edit.com": "This is a placeholder for the edit.com executable file.",
                        "mouse.sys": "This is a placeholder for the mouse.sys driver file."
                    },
                    "folders": {}
                },
                "temp": {}
            }
        }
        save_vfs(empty_vfs)
        return "Disk drive C: initialized."
    return "Disk drive C: ready."

def save_vfs(vfs):
    with open(VFS_PATH, "w") as f:
        json.dump(vfs, f, indent=4)

def load_vfs():
    if os.path.exists(VFS_PATH):
        with open(VFS_PATH, "r") as f:
            return json.load(f)
    else:
        return None

def update_used_space(vfs):
    total = 0
    def calculate(node):
        nonlocal total
        # Files are just strings, so f is the content
        for f in node.get("files", {}).values():
            total += len(str(f))

        # Recurse into folders
        for fld in node.get("folders", {}).values():
            calculate(fld)
            
    calculate(vfs)
    vfs["metadata"]["used_size_bytes"] = total