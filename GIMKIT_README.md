# Sorter - File Management Tool

## Product Overview

**Sorter** is a modern, intelligent file management application that helps you organize, find, and manage files on your computer with ease. It features three powerful tools: Keyword Sorter, TimeSort, and SmartSort.

---

## System Requirements

| Requirement | Details |
|---|---|
| **Operating System** | Windows 10/11 (64-bit) |
| **Processor** | Intel/AMD 1.5 GHz or faster |
| **RAM** | 2 GB minimum, 4 GB recommended |
| **Disk Space** | 100 MB for installation |
| **Python** (if running from source) | Python 3.8 or higher |

---

## Download & Installation

### Option 1: Standalone Executable (Recommended)
**Download:** [Sorter.exe](https://github.com/sorter/releases/download/v1.0.0/Sorter.exe)

1. Download `Sorter.exe`
2. Double-click to run
3. Grant file explorer access permission when prompted
4. Start using immediately - no installation required

### Option 2: From Source (Python)
**Requirements:** Python 3.8+

```bash
# Clone or download the repository
git clone https://github.com/your-repo/Sorter.git
cd Sorter

# Install dependencies
pip install -r Sorter/requirements.txt
pip install -r "Smart Sorter/requirements.txt"

# Run the application
python Sorter/main.py
```

---

## Product Features

### 🔍 Keyword Sorter
Find files by keyword with intelligent matching
- Search for files containing specific keywords
- Case-insensitive matching (finds "BACKUP", "backup", "Backup")
- Automatic plural detection (search "backups" finds "backup" too)
- Batch delete, copy, or move files
- Multi-select with checkboxes

### ⏰ TimeSort
Find and manage old files
- Locate files not accessed in X days
- See exact last access dates and times
- Delete, copy, or move old files in bulk
- Customizable time threshold (1-3650 days)

### 🧠 SmartSort
Intelligent file organization
- Analyzes files by name patterns
- Suggests 5 organization strategies
- Preview folder structure before applying
- One-click automatic organization

---

## How to Use

### Getting Started

1. **Launch the app** - Double-click `Sorter.exe` or run `python Sorter/main.py`
2. **Grant permission** - Click "Allow Access" on the first launch
3. **Choose a tool** - Select from three tabs at the top

### Keyword Sorter

**Step 1:** Click "📁 Select Folder" and choose a directory to search

**Step 2:** Enter a keyword (e.g., "backup", "project", "temp")

**Step 3:** Click "🔍 Search" or press Enter

**Step 4:** Click files to select them (checkboxes appear)

**Step 5:** Choose an action:
- **🗑️ Delete Selected** - Remove files permanently
- **📋 Copy Selected** - Copy to another location
- **📦 Move to Folder** - Move to a new folder

### TimeSort

**Step 1:** Click "📁 Select Folder" to choose a directory

**Step 2:** Set the number of days (default: 30 days)

**Step 3:** Click "🔍 Scan" to find old files

**Step 4:** Select files from the results

**Step 5:** Choose an action:
- **🗑️ Delete Selected** - Remove old files
- **📋 Copy Selected** - Archive old files
- **📦 Move Selected** - Move to backup location

### SmartSort

**Step 1:** Click "📁 Select Folder" to analyze

**Step 2:** Click "🔍 Analyze" to scan files

**Step 3:** Select an organization suggestion from the dropdown

**Step 4:** Click "👁️ Preview Structure" to see the folder layout

**Step 5:** Click "✓ Apply Organization" to create folders and move files

**Available suggestions:**
- By File Type (groups by extension: .pdf, .jpg, .docx, etc.)
- By Project/Prefix (groups by filename prefix)
- By Date (groups files with date patterns)
- By Version (groups versioned files: v1, v2, etc.)
- Single Folder (moves all to one organized folder)

---

## Command-Line Alternatives

### PowerShell Commands

```powershell
# Search for files by keyword
.\Sorter\sorter.ps1 -Folder "C:\Users\YourName\Documents" -Keyword "backup" -Action list

# Delete matching files
.\Sorter\sorter.ps1 -Folder "C:\path" -Keyword "backup" -Action delete

# Copy matching files
.\Sorter\sorter.ps1 -Folder "C:\path" -Keyword "backup" -Action copy -Destination "C:\destination"

# Move matching files
.\Sorter\sorter.ps1 -Folder "C:\path" -Keyword "backup" -Action move -Destination "C:\destination"

# Case-sensitive search (no plural matching)
.\Sorter\sorter.ps1 -Folder "C:\path" -Keyword "Backup" -Action list -CaseSensitive -NoPlural
```

### Python Commands

```python
# Import the Sorter module
from Sorter import sort

# List matching files
results = sort.folder("C:/Users/YourName/Documents", "backup")
print(f"Found {len(results)} items")

# Delete matching files
deleted = sort.delete("C:/path", "backup")
print(f"Deleted {deleted} items")

# Copy matching files
copied = sort.copy("C:/path", "backup", "C:/destination")

# Move matching files
moved = sort.move("C:/path", "backup", "C:/destination")
```

**TimeSort Python:**
```python
from Smart_Sorter import TimeSort

# Find files not accessed in 30 days
results = TimeSort("C:/Users/YourName/Documents", 30)
print(f"Found {len(results)} old items")

# Delete old files
deleted = results.delete()
```

**SmartSort Python:**
```python
from Smart_Sorter import SmartSort

# Analyze files
analysis = SmartSort("C:/Users/YourName/Downloads")

# View suggestions
for i, suggestion in enumerate(analysis.suggestions):
    print(f"{i}: {suggestion['name']}")

# Apply a suggestion
result = analysis.apply_structure(0)
print(f"Moved {result['moved_files']} files")
```

---

## Settings

Access settings by clicking "⚙️ Settings" in the Keyword Sorter tab:

- **Case Sensitive** - Toggle case-sensitive file matching
- **Include Plural Forms** - Automatically search for plural variations
- **Theme** - Switch between Dark and Light themes

---

## Privacy & Security

✓ **Local Processing** - All operations happen on your computer
✓ **No Data Transmission** - Nothing is sent to external servers
✓ **No File Content Reading** - We only read filenames and metadata
✓ **Permission-Based** - You control what the app can access
⚠️ **Security Notice** - If this app is compromised, file safety cannot be guaranteed

---

## Troubleshooting

### App won't start
- Ensure Windows 10/11 is installed
- Try running as Administrator
- Restart your computer

### Permission denied on first launch
- Click "Allow Access" to grant file explorer permission
- If you clicked "Deny", restart the app and grant permission

### Files not found
- Ensure the folder path is correct
- Check that you have read permissions for the folder
- Try a simpler keyword

### App is slow
- Close other applications to free up RAM
- Avoid searching very large folders (1M+ files)
- Try searching a specific subfolder instead

---

## License

Licensed under the MIT License - free to use, modify, and distribute.

---

## Support & Feedback

For issues, questions, or feature requests, please visit the project repository or contact support.

**Version:** 1.0.0  
**Last Updated:** December 2025  
**Made with ❤️ for better file management**
