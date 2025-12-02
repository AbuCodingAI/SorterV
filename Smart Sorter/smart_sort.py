"""
SmartSort - Analyze files by name and suggest folder organization structures
Usage: from Smart_Sorter import SmartSort
        SmartSort(folder_location)
"""

import os
from pathlib import Path
from collections import defaultdict
import re


class SmartSortAnalysis:
    """Container for SmartSort analysis results"""
    def __init__(self, folder, file_groups, suggestions):
        self.folder = folder
        self.file_groups = file_groups
        self.suggestions = suggestions
    
    def __repr__(self):
        return f"SmartSortAnalysis(groups={len(self.file_groups)}, suggestions={len(self.suggestions)})"
    
    def get_suggestion(self, index):
        """Get a specific suggestion"""
        if 0 <= index < len(self.suggestions):
            return self.suggestions[index]
        return None
    
    def apply_structure(self, suggestion_index, base_folder=None):
        """Apply the suggested folder structure"""
        if base_folder is None:
            base_folder = self.folder
        
        suggestion = self.get_suggestion(suggestion_index)
        if not suggestion:
            raise ValueError("Invalid suggestion index")
        
        structure = suggestion["structure"]
        created_folders = []
        moved_files = 0
        
        import shutil
        
        for group_name, files in self.file_groups.items():
            if group_name in structure:
                folder_path = os.path.join(base_folder, structure[group_name])
                os.makedirs(folder_path, exist_ok=True)
                created_folders.append(folder_path)
                
                for file_path in files:
                    try:
                        dest_path = os.path.join(folder_path, os.path.basename(file_path))
                        shutil.move(file_path, dest_path)
                        moved_files += 1
                    except Exception as e:
                        print(f"Error moving {file_path}: {e}")
        
        return {
            "created_folders": created_folders,
            "moved_files": moved_files
        }


def _extract_patterns(files):
    """Extract common patterns from filenames"""
    patterns = defaultdict(list)
    
    for file_path in files:
        filename = os.path.basename(file_path)
        name_without_ext = os.path.splitext(filename)[0]
        ext = os.path.splitext(filename)[1].lower()
        
        # Group by extension
        if ext:
            patterns[f"By Extension: {ext}"].append(file_path)
        
        # Group by prefix (first word)
        words = re.split(r'[_\-\s]+', name_without_ext)
        if words and words[0]:
            patterns[f"By Prefix: {words[0]}"].append(file_path)
        
        # Group by date pattern (YYYY-MM-DD or YYYYMMDD)
        date_match = re.search(r'\d{4}[-_]?\d{2}[-_]?\d{2}', filename)
        if date_match:
            patterns["By Date"].append(file_path)
        
        # Group by version pattern (v1, v2, etc.)
        version_match = re.search(r'v\d+', filename, re.IGNORECASE)
        if version_match:
            patterns["By Version"].append(file_path)
    
    return patterns


def _generate_suggestions(file_groups):
    """Generate folder organization suggestions"""
    suggestions = []
    
    # Suggestion 1: By Extension
    ext_structure = {}
    for group_name in file_groups:
        if group_name.startswith("By Extension:"):
            ext = group_name.replace("By Extension: ", "").replace(".", "")
            ext_structure[group_name] = f"By Type/{ext if ext else 'No Extension'}"
    
    if ext_structure:
        suggestions.append({
            "name": "Organize by File Type",
            "description": "Group files by their extension (images, documents, etc.)",
            "structure": ext_structure
        })
    
    # Suggestion 2: By Prefix
    prefix_structure = {}
    for group_name in file_groups:
        if group_name.startswith("By Prefix:"):
            prefix = group_name.replace("By Prefix: ", "")
            prefix_structure[group_name] = f"By Project/{prefix}"
    
    if prefix_structure:
        suggestions.append({
            "name": "Organize by Project/Prefix",
            "description": "Group files by their naming prefix (project names, etc.)",
            "structure": prefix_structure
        })
    
    # Suggestion 3: By Date
    if "By Date" in file_groups:
        suggestions.append({
            "name": "Organize by Date",
            "description": "Group files by date patterns found in filenames",
            "structure": {"By Date": "By Date"}
        })
    
    # Suggestion 4: By Version
    if "By Version" in file_groups:
        suggestions.append({
            "name": "Organize by Version",
            "description": "Group versioned files together",
            "structure": {"By Version": "Versions"}
        })
    
    # Suggestion 5: Custom - All in one folder
    custom_structure = {group: "Organized Files" for group in file_groups}
    suggestions.append({
        "name": "Move All to Single Folder",
        "description": "Move all files to a single 'Organized Files' folder",
        "structure": custom_structure
    })
    
    return suggestions


def SmartSort(folder_location):
    """
    Analyze files by name and suggest folder organization structures
    
    Args:
        folder_location (str): Path to analyze
    
    Returns:
        SmartSortAnalysis: Object containing analysis and suggestions
    
    Example:
        analysis = SmartSort("C:/Users/Abu/Downloads")
        
        # View suggestions
        for i, suggestion in enumerate(analysis.suggestions):
            print(f"{i}: {suggestion['name']}")
            print(f"   {suggestion['description']}")
        
        # Apply a suggestion
        result = analysis.apply_structure(0)
        print(f"Created {len(result['created_folders'])} folders")
        print(f"Moved {result['moved_files']} files")
    """
    if not os.path.exists(folder_location):
        raise ValueError(f"Folder not found: {folder_location}")
    
    # Collect all files
    all_files = []
    for root, dirs, files in os.walk(folder_location):
        for file_name in files:
            all_files.append(os.path.join(root, file_name))
    
    if not all_files:
        raise ValueError("No files found in folder")
    
    # Extract patterns
    file_groups = _extract_patterns(all_files)
    
    # Generate suggestions
    suggestions = _generate_suggestions(file_groups)
    
    return SmartSortAnalysis(folder_location, file_groups, suggestions)
