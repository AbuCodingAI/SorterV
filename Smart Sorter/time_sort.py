"""
TimeSort - Find files not accessed in X days
Usage: from Smart_Sorter import TimeSort
        TimeSort(folder_location, days)
"""

import os
import time
from datetime import datetime, timedelta
from pathlib import Path


class TimeSortResults:
    """Container for TimeSort results"""
    def __init__(self, files, days, folder):
        self.files = files
        self.days = days
        self.folder = folder
        self.cutoff_time = time.time() - (days * 86400)
    
    def __repr__(self):
        return f"TimeSortResults(found={len(self.files)}, days={self.days})"
    
    def __len__(self):
        return len(self.files)
    
    def __iter__(self):
        return iter(self.files)
    
    def get_details(self):
        """Get detailed info about each file (path, last accessed, days ago)"""
        details = []
        for file_path in self.files:
            try:
                stat = os.stat(file_path)
                last_access = stat.st_atime
                days_ago = (time.time() - last_access) / 86400
                last_access_date = datetime.fromtimestamp(last_access).strftime("%Y-%m-%d %H:%M:%S")
                
                details.append({
                    "path": file_path,
                    "last_accessed": last_access_date,
                    "days_ago": round(days_ago, 1),
                    "is_dir": os.path.isdir(file_path)
                })
            except Exception as e:
                print(f"Error getting details for {file_path}: {e}")
        
        return details
    
    def delete(self):
        """Delete all found files/folders"""
        import shutil
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
        import shutil
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
        import shutil
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


def TimeSort(folder_location, days):
    """
    Find all files/folders not accessed in X days
    
    Args:
        folder_location (str): Path to search in
        days (int): Number of days of inactivity
    
    Returns:
        TimeSortResults: Object containing found files with methods (delete, copy, move, get_details)
    
    Example:
        results = TimeSort("C:/Users/Abu/Documents", 30)
        print(f"Found {len(results)} items not accessed in 30 days")
        
        # View details
        for item in results.get_details():
            print(f"{item['path']} - Last accessed: {item['last_accessed']} ({item['days_ago']} days ago)")
        
        # Delete old files
        deleted = results.delete()
        print(f"Deleted {deleted} items")
    """
    if not os.path.exists(folder_location):
        raise ValueError(f"Folder not found: {folder_location}")
    
    if days <= 0:
        raise ValueError("Days must be greater than 0")
    
    cutoff_time = time.time() - (days * 86400)
    results = []
    
    for root, dirs, files in os.walk(folder_location):
        # Check directories
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            try:
                stat = os.stat(dir_path)
                if stat.st_atime < cutoff_time:
                    results.append(dir_path)
            except Exception as e:
                print(f"Error checking {dir_path}: {e}")
        
        # Check files
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                stat = os.stat(file_path)
                if stat.st_atime < cutoff_time:
                    results.append(file_path)
            except Exception as e:
                print(f"Error checking {file_path}: {e}")
    
    return TimeSortResults(results, days, folder_location)
