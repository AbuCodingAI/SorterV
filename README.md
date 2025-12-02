# Sorter - Intelligent File Management Tool

A modern, glossy desktop application for finding, organizing, and managing files with three powerful tools: Keyword Sorter, TimeSort, and SmartSort.

## Features

### 🔍 Keyword Sorter
Search for files and folders by keyword with intelligent matching:
- **Case-insensitive search** - Find "BACKUP", "backup", "Backup" all at once
- **Plural detection** - Search "backups" to find both "backup" and "backups"
- **Batch operations** - Delete, copy, or move multiple files at once
- **Multi-select** - Use checkboxes to select specific files

### ⏰ TimeSort
Find and manage files based on access time:
- **Find old files** - Locate files not accessed in X days
- **Detailed timestamps** - See exactly when each file was last accessed
- **Batch actions** - Delete, copy, or move old files
- **Customizable threshold** - Set any number of days (1-3650)

### 🧠 SmartSort
Intelligent file organization by analyzing name patterns:
- **Pattern detection** - Automatically identifies file types, prefixes, dates, and versions
- **Smart suggestions** - Get 5 organization strategies:
  - By File Type (extensions)
  - By Project/Prefix
  - By Date patterns
  - By Version
  - Single folder organization
- **Preview before applying** - See the folder structure before making changes
- **One-click organization** - Apply suggestions to automatically create folders and move files

## Installation

### Requirements
- Python 3.8+
- PyQt6

### Setup

1. Clone or download the repository
2. Install dependencies:
```bash
pip install -r Sorter/requirements.txt
pip install -r "Smart Sorter/requirements.txt"
```

3. Run the application:
```bash
python Sorter/main.py
```

## Usage

### First Launch
On first launch, the app will ask for **file explorer access permission**. This is required to:
- Search for files
- Organize files
- Perform file operations

**Privacy Promise:**
- ✓ We will NOT read file contents unless you explicitly ask
- ✓ We will NOT upload or transmit any data
- ✓ We will NOT access files outside your selected folder
- ✓ All operations are local to your machine
- ⚠️ If hacked, file safety cannot be guaranteed

### Keyword Sorter Tab

1. Click **"📁 Select Folder"** to choose a directory
2. Enter a **keyword** (e.g., "backup", "project", "temp")
3. Click **"🔍 Search"** or press Enter
4. Click items to select them (checkboxes appear)
5. Choose an action:
   - **🗑️ Delete Selected** - Remove files permanently
   - **📋 Copy Selected** - Copy to another location
   - **📦 Move to Folder** - Move to a new folder
   - **Clear Selection** - Deselect all

**Settings:**
- **Case Sensitive** - Toggle case-sensitive matching
- **Include Plural Forms** - Automatically search for plural variations
- **Theme** - Switch between Dark and Light themes

### TimeSort Tab

1. Click **"📁 Select Folder"** to choose a directory
2. Set the **number of days** (default: 30)
3. Click **"🔍 Scan"** to find old files
4. Results show files with last access date and days ago
5. Select files and choose an action:
   - **🗑️ Delete Selected** - Remove old files
   - **📋 Copy Selected** - Archive old files
   - **📦 Move Selected** - Move to backup location

### SmartSort Tab

1. Click **"📁 Select Folder"** to analyze
2. Click **"🔍 Analyze"** to scan files
3. View **organization suggestions** in the dropdown
4. Read the **description** of each suggestion
5. Click **"👁️ Preview Structure"** to see the folder layout
6. Click **"✓ Apply Organization"** to create folders and move files

**Suggestions include:**
- By File Type - Groups by extension (.pdf, .jpg, .docx, etc.)
- By Project/Prefix - Groups by filename prefix
- By Date - Groups files with date patterns
- By Version - Groups versioned files (v1, v2, etc.)
- Single Folder - Moves all to one organized folder

## Building to .exe

### Quick Build

To create a standalone executable:

```bash
cd Sorter
python build.py
```

The executable will be created in `dist/Sorter.exe`

### How to Build from Source

**Requirements:**
- Python 3.8+
- PyQt6
- PyInstaller

**Step-by-step:**

1. **Clone the repository**
```bash
git clone https://github.com/your-repo/Sorter.git
cd Sorter
```

2. **Install dependencies**
```bash
pip install -r Sorter/requirements.txt
pip install -r "Smart Sorter/requirements.txt"
```

3. **Test the app**
```bash
python Sorter/main.py
```

4. **Build the executable**
```bash
cd Sorter
python build.py
```

5. **Find your executable**
- Location: `Sorter/dist/Sorter.exe`
- Size: ~35 MB

### Customizing the Build

Edit `Sorter/build.py` to customize:
- Icon: `--icon=path/to/icon.ico`
- Name: `--name=YourAppName`
- Console: Remove `--windowed` to show console
- One-file: Change `--onefile` to `--onedir` for folder distribution

### Splitting for GitHub

If the exe is too large for GitHub (>25 MB):

```bash
# Split the exe
$exe = [System.IO.File]::ReadAllBytes("Sorter/dist/Sorter.exe")
$half = [math]::Floor($exe.Length / 2)
[System.IO.File]::WriteAllBytes("Sorter/dist/Sorter.exe.part1", $exe[0..($half-1)])
[System.IO.File]::WriteAllBytes("Sorter/dist/Sorter.exe.part2", $exe[$half..($exe.Length-1)])
```

Users then run `construct.bat` to reassemble.

## Project Structure

```
Sorter/
├── main.py                 # Main GUI application
├── file_scanner.py         # Keyword search logic
├── sort.py                 # Python API for keyword sorting
├── ui_theme.py             # Modern dark theme styling
├── build.py                # Build script for .exe
├── __init__.py             # Package initialization
├── requirements.txt        # Python dependencies
└── config.json             # User settings (auto-generated)

Smart Sorter/
├── smart_sort.py           # SmartSort analysis engine
├── smart_sort_gui.py       # SmartSort GUI widget
├── time_sort.py            # TimeSort engine
├── time_sort_gui.py        # TimeSort GUI widget
├── __init__.py             # Package initialization
└── requirements.txt        # Dependencies
```

## Python API

Sorter includes a Python API in `Sorter/sort.py` for programmatic file management. You can import and use it in your own Python scripts:

### Keyword Sorting API
```python
from Sorter import sort

# List matching files
results = sort.folder("C:/Users/Abu/Documents", "backup")
print(f"Found {len(results)} items")
for file_path in results:
    print(file_path)

# Delete matching files
deleted = sort.delete("C:/path", "backup")
print(f"Deleted {deleted} items")

# Copy matching files
copied = sort.copy("C:/path", "backup", "C:/destination")
print(f"Copied {copied} items")

# Move matching files
moved = sort.move("C:/path", "backup", "C:/destination")
print(f"Moved {moved} items")

# Advanced: Use results object with methods
results = sort.folder("C:/path", "backup", case_sensitive=False, include_plural=True)
results.delete()  # or results.copy("dest") or results.move("dest")
```

### TimeSort API
```python
from Smart_Sorter import TimeSort

# Find old files
results = TimeSort("C:/Users/Abu/Documents", 30)
print(f"Found {len(results)} items not accessed in 30 days")

# View details with timestamps
for item in results.get_details():
    print(f"{item['path']}")
    print(f"  Last accessed: {item['last_accessed']}")
    print(f"  Days ago: {item['days_ago']}")

# Delete old files
deleted = results.delete()

# Copy old files to archive
copied = results.copy("C:/Archive")

# Move old files to backup
moved = results.move("C:/Backup")
```

### SmartSort API
```python
from Smart_Sorter import SmartSort

# Analyze files
analysis = SmartSort("C:/Users/Abu/Downloads")

# View all suggestions
for i, suggestion in enumerate(analysis.suggestions):
    print(f"{i}: {suggestion['name']}")
    print(f"   {suggestion['description']}")

# Apply a specific suggestion
result = analysis.apply_structure(0)
print(f"Created {len(result['created_folders'])} folders")
print(f"Moved {result['moved_files']} files")
```

## PowerShell Commands

Use Sorter from PowerShell:

```powershell
# List matching files
.\Sorter\sorter.ps1 -Folder "C:\path" -Keyword "backup" -Action list

# Delete matching files
.\Sorter\sorter.ps1 -Folder "C:\path" -Keyword "backup" -Action delete

# Copy matching files
.\Sorter\sorter.ps1 -Folder "C:\path" -Keyword "backup" -Action copy -Destination "C:\destination"

# Move matching files
.\Sorter\sorter.ps1 -Folder "C:\path" -Keyword "backup" -Action move -Destination "C:\destination"

# Case-sensitive search
.\Sorter\sorter.ps1 -Folder "C:\path" -Keyword "Backup" -Action list -CaseSensitive -NoPlural
```

## Settings

Settings are saved in `config.json`:
- **last_folder** - Last selected folder
- **case_sensitive** - Case-sensitive search (default: false)
- **include_plural** - Include plural forms (default: true)
- **theme** - UI theme (default: dark)
- **file_access_permission_granted** - Permission status

## UI Theme

The app features a modern, glossy dark theme with:
- Clean teal accents (#0d7377)
- Smooth rounded corners
- Responsive hover effects
- Professional color scheme
- Accessibility-compliant contrast

## Security & Privacy

- **Local processing only** - All operations happen on your machine
- **No data transmission** - Nothing is sent to external servers
- **Open source** - Code is available for verification
- **Permission-based** - Asks for file access on first launch
- **Configurable** - You control what the app can access

## Troubleshooting

### App won't start
- Ensure Python 3.8+ is installed
- Verify PyQt6 is installed: `pip install PyQt6`
- Check that you're in the correct directory

### Permission denied on first launch
- Click "Allow Access" to grant file explorer permission
- If denied, restart the app and grant permission

### Files not found
- Ensure the folder path is correct
- Check that you have read permissions for the folder
- Try a simpler keyword first

### Build to .exe fails
- Ensure PyInstaller is installed: `pip install pyinstaller`
- Run from the Sorter directory
- Check that all dependencies are installed

## Future Enhancements

- Advanced filtering options
- File preview functionality
- Undo/Redo operations
- Search history
- Custom themes
- Scheduled cleanup tasks
- File comparison tools
- Duplicate file detection

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

You are free to:
- ✓ Use commercially
- ✓ Modify the code
- ✓ Distribute copies
- ✓ Use privately

With the condition that you include the license and copyright notice.

## Support

For issues, questions, or suggestions, please check the code or create an issue in the repository.

---

**Made with ❤️ for better file management**
