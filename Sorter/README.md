# Sorter - File Management Tool

A modern, glossy desktop application for finding and managing files by keyword with a refined UI.

## Features

- **Keyword Search**: Search for files/folders containing a keyword (case-insensitive by default)
- **Smart Matching**: 
  - Case-insensitive search (BacKuPS finds BACKUPS, backups, Backups)
  - Plural form detection (searching "backups" also finds "backup")
- **Batch Operations**:
  - Delete selected files/folders
  - Copy to destination
  - Move to a new folder
  - Multi-select with Ctrl+Click
- **Modern UI**: Dark theme with glossy, clean design
- **Customizable Settings**: Toggle case sensitivity, plural matching, theme

## Installation

### Requirements
- Python 3.8+
- PyQt6

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

## Building to .exe

To compile into a standalone executable:

```bash
python build.py
```

The executable will be created in the `dist/` folder.

## Usage

1. Click "📁 Select Folder" to choose the directory to search
2. Enter a keyword (e.g., "backup")
3. Click "🔍 Search" or press Enter
4. Click items to select them (Ctrl+Click for multi-select)
5. Choose an action:
   - **Delete**: Remove selected files/folders
   - **Copy**: Copy to another location
   - **Move to Folder**: Move all selected items to a new folder

## Settings

- **Case Sensitive**: Toggle case-sensitive matching
- **Include Plural Forms**: Automatically search for plural variations
- **Theme**: Switch between Dark and Light themes

## Project Structure

```
Sorter/
├── main.py              # Main application window
├── file_scanner.py      # File search logic
├── ui_theme.py          # Modern theme styling
├── build.py             # Build script for .exe
├── config.json          # User settings (auto-generated)
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Future Enhancements

- Command-line interface
- Advanced filtering options
- File preview
- Undo/Redo functionality
- Custom themes
- Search history
