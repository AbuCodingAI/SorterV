"""
Build script to compile Sorter into a standalone .exe
Run: python build.py
"""

import subprocess
import os
import sys

def build_exe():
    print("Building Sorter.exe...")
    
    # Get the parent directory to include SmartSort
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    smart_sorter_path = os.path.join(parent_dir, "Smart Sorter")
    
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--windowed",
        "--name=Sorter",
        "--add-data=config.json:.",
        f"--path={smart_sorter_path}",
        "main.py"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("\n✓ Build successful!")
        print("Executable location: dist/Sorter.exe")
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Build failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_exe()
