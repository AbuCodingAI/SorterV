import os
from pathlib import Path
from PyQt6.QtCore import QThread, pyqtSignal


class FileScanner(QThread):
    results_found = pyqtSignal(list)
    
    def __init__(self, root_path, keyword, case_sensitive=False, include_plural=True):
        super().__init__()
        self.root_path = root_path
        self.keyword = keyword
        self.case_sensitive = case_sensitive
        self.include_plural = include_plural
        self.results = []
    
    def run(self):
        self.results = []
        search_keywords = self.generate_search_keywords()
        
        for root, dirs, files in os.walk(self.root_path):
            # Search in directories
            for dir_name in dirs:
                if self.matches_keyword(dir_name, search_keywords):
                    self.results.append(os.path.join(root, dir_name))
            
            # Search in files
            for file_name in files:
                if self.matches_keyword(file_name, search_keywords):
                    self.results.append(os.path.join(root, file_name))
        
        self.results_found.emit(self.results)
    
    def generate_search_keywords(self):
        keywords = [self.keyword]
        
        if not self.case_sensitive:
            keywords.append(self.keyword.lower())
            keywords.append(self.keyword.upper())
            keywords.append(self.keyword.capitalize())
        
        if self.include_plural and self.keyword.endswith('s'):
            base = self.keyword[:-1]
            keywords.append(base)
            if not self.case_sensitive:
                keywords.append(base.lower())
                keywords.append(base.upper())
                keywords.append(base.capitalize())
        
        return list(set(keywords))
    
    def matches_keyword(self, name, keywords):
        for keyword in keywords:
            if keyword in name:
                return True
        return False
