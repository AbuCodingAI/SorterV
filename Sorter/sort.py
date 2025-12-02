"""
Sorter API - Command-line and programmatic interface for file sorting
Usage: from Sorter import sort
        sort.folder(folder_location, keyword, action="list")
"""

import os
import shutil
from pathlib import Path


class SortResults:
    """Container for sort results"""
    def __init__(self, files, keyword, folder):
        self.files = files
        self.keyword = keyword
        self.folder = folder
    
    def __repr__(self):
        return f"SortResults(found={len(self.files)}, keyword='{self.keyword}')"
    
    def __len__(self):
        return len(self.files)
    
    def __iter__(self):
        return iter(self.files)
    
    def delete(self):
        """Delete all found files/folders"""
        deleted = 0
        for file_path in self.files:
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                deleted += 1
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
        return deleted
    
    def copy(self, destination):
        """Copy all found files/folders to destination"""
        os.makedirs(destination, exist_ok=True)
        copied = 0
        for file_path in self.files:
            try:
                dest_path = os.path.join(destination, os.path.basename(file_path))
                if os.path.isfile(file_path):
                    shutil.copy2(file_path, dest_path)
                elif os.path.isdir(file_path):
                    shutil.copytree(file_path, dest_path)
                copied += 1
            except Exception as e:
                print(f"Error copying {file_path}: {e}")
        return copied
    
    def move(self, destination):
        """Move all found files/folders to destination"""
        os.makedirs(destination, exist_ok=True)
        moved = 0
        for file_path in self.files:
            try:
                dest_path = os.path.join(destination, os.path.basename(file_path))
                shutil.move(file_path, dest_path)
                moved += 1
            except Exception as e:
                print(f"Error moving {file_path}: {e}")
        return moved


def _generate_keywords(keyword, case_sensitive=False, include_plural=True):
    """Generate search keywords based on settings"""
    keywords = [keyword]
    
    if not case_sensitive:
        keywords.append(keyword.lower())
        keywords.append(keyword.upper())
        keywords.append(keyword.capitalize())
    
    if include_plural and keyword.endswith('s'):
        base = keyword[:-1]
        keywords.append(base)
        if not case_sensitive:
            keywords.append(base.lower())
            keywords.append(base.upper())
            keywords.append(base.capitalize())
    
    return list(set(keywords))


def _matches_keyword(name, keywords):
    """Check if name matches any keyword"""
    for keyword in keywords:
        if keyword in name:
            return True
    return False


def folder(folder_location, keyword, case_sensitive=False, include_plural=True):
    """
    Search for files/folders by keyword
    
    Args:
        folder_location (str): Path to search in
        keyword (str): Keyword to search for
        case_sensitive (bool): Case-sensitive search (default: False)
        include_plural (bool): Include plural forms (default: True)
    
    Returns:
        SortResults: Object containing found files with methods (delete, copy, move)
    
    Example:
        results = sort.folder("C:/Users/Abu/Documents", "backup")
        print(f"Found {len(results)} items")
        results.delete()
    """
    if not os.path.exists(folder_location):
        raise ValueError(f"Folder not found: {folder_location}")
    
    if not keyword:
        raise ValueError("Keyword cannot be empty")
    
    results = []
    search_keywords = _generate_keywords(keyword, case_sensitive, include_plural)
    
    for root, dirs, files in os.walk(folder_location):
        # Search directories
        for dir_name in dirs:
            if _matches_keyword(dir_name, search_keywords):
                results.append(os.path.join(root, dir_name))
        
        # Search files
        for file_name in files:
            if _matches_keyword(file_name, search_keywords):
                results.append(os.path.join(root, file_name))
    
    return SortResults(results, keyword, folder_location)


def list_files(folder_location, keyword, case_sensitive=False, include_plural=True):
    """
    Get list of files matching keyword
    
    Returns:
        list: File paths
    """
    results = folder(folder_location, keyword, case_sensitive, include_plural)
    return list(results.files)


def delete(folder_location, keyword, case_sensitive=False, include_plural=True):
    """Delete all files matching keyword"""
    results = folder(folder_location, keyword, case_sensitive, include_plural)
    return results.delete()


def copy(folder_location, keyword, destination, case_sensitive=False, include_plural=True):
    """Copy all files matching keyword to destination"""
    results = folder(folder_location, keyword, case_sensitive, include_plural)
    return results.copy(destination)


def move(folder_location, keyword, destination, case_sensitive=False, include_plural=True):
    """Move all files matching keyword to destination"""
    results = folder(folder_location, keyword, case_sensitive, include_plural)
    return results.move(destination)
