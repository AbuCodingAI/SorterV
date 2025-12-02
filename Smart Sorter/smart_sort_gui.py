"""
SmartSort GUI - Analyze and organize files by name patterns
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QFileDialog, QMessageBox, QTextEdit,
    QComboBox, QSpinBox, QDialog, QScrollArea
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont
import os
from smart_sort import SmartSort


class SmartSortAnalyzer(QThread):
    """Background thread for analyzing files"""
    analysis_complete = pyqtSignal(object)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path
    
    def run(self):
        try:
            analysis = SmartSort(self.folder_path)
            self.analysis_complete.emit(analysis)
        except Exception as e:
            self.error_occurred.emit(str(e))


class SmartSortWidget(QWidget):
    """SmartSort GUI Widget"""
    
    def __init__(self):
        super().__init__()
        self.current_analysis = None
        self.analyzer_thread = None
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Header
        header_label = QLabel("SmartSort - Intelligent File Organization")
        header_font = QFont()
        header_font.setPointSize(14)
        header_font.setBold(True)
        header_label.setFont(header_font)
        layout.addWidget(header_label)
        
        # Folder selection
        folder_layout = QHBoxLayout()
        folder_btn = QPushButton("📁 Select Folder")
        folder_btn.clicked.connect(self.select_folder)
        folder_btn.setMinimumHeight(40)
        folder_layout.addWidget(folder_btn)
        
        self.folder_label = QLabel("No folder selected")
        self.folder_label.setStyleSheet("color: #888; font-style: italic;")
        folder_layout.addWidget(self.folder_label)
        
        analyze_btn = QPushButton("🔍 Analyze")
        analyze_btn.clicked.connect(self.analyze_files)
        analyze_btn.setMinimumHeight(40)
        folder_layout.addWidget(analyze_btn)
        
        layout.addLayout(folder_layout)
        
        # Suggestions section
        suggestions_label = QLabel("Organization Suggestions:")
        layout.addWidget(suggestions_label)
        
        suggestions_layout = QHBoxLayout()
        suggestions_layout.addWidget(QLabel("Choose a suggestion:"))
        
        self.suggestion_combo = QComboBox()
        self.suggestion_combo.currentIndexChanged.connect(self.on_suggestion_changed)
        suggestions_layout.addWidget(self.suggestion_combo)
        
        layout.addLayout(suggestions_layout)
        
        # Description
        self.description_text = QTextEdit()
        self.description_text.setReadOnly(True)
        self.description_text.setMaximumHeight(80)
        layout.addWidget(self.description_text)
        
        # Preview
        preview_label = QLabel("File Groups Preview:")
        layout.addWidget(preview_label)
        
        self.preview_list = QListWidget()
        layout.addWidget(self.preview_list)
        
        # Status
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        apply_btn = QPushButton("✓ Apply Organization")
        apply_btn.clicked.connect(self.apply_suggestion)
        action_layout.addWidget(apply_btn)
        
        preview_btn = QPushButton("👁️ Preview Structure")
        preview_btn.clicked.connect(self.preview_structure)
        action_layout.addWidget(preview_btn)
        
        layout.addLayout(action_layout)
        
        self.setLayout(layout)
    
    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder to Analyze")
        if folder:
            self.folder_label.setText(f"📂 {folder}")
            self.status_label.setText("Folder selected. Click Analyze to start.")
    
    def analyze_files(self):
        folder = self.folder_label.text()
        if folder == "No folder selected" or not folder.startswith("📂"):
            QMessageBox.warning(self, "No Folder", "Please select a folder first.")
            return
        
        folder_path = folder.replace("📂 ", "")
        
        self.status_label.setText("Analyzing files...")
        self.suggestion_combo.clear()
        self.preview_list.clear()
        self.description_text.clear()
        
        self.analyzer_thread = SmartSortAnalyzer(folder_path)
        self.analyzer_thread.analysis_complete.connect(self.display_analysis)
        self.analyzer_thread.error_occurred.connect(self.handle_error)
        self.analyzer_thread.finished.connect(self.analysis_finished)
        self.analyzer_thread.start()
    
    def display_analysis(self, analysis):
        self.current_analysis = analysis
        
        # Populate suggestions
        for i, suggestion in enumerate(analysis.suggestions):
            self.suggestion_combo.addItem(suggestion["name"], i)
        
        self.on_suggestion_changed(0)
    
    def on_suggestion_changed(self, index):
        if not self.current_analysis or index < 0:
            return
        
        suggestion = self.current_analysis.suggestions[index]
        
        # Update description
        self.description_text.setText(suggestion["description"])
        
        # Update preview
        self.preview_list.clear()
        structure = suggestion["structure"]
        
        for group_name, folder_path in structure.items():
            if group_name in self.current_analysis.file_groups:
                file_count = len(self.current_analysis.file_groups[group_name])
                item_text = f"📁 {folder_path} ({file_count} files)"
                self.preview_list.addItem(item_text)
    
    def preview_structure(self):
        if not self.current_analysis:
            QMessageBox.warning(self, "No Analysis", "Please analyze files first.")
            return
        
        index = self.suggestion_combo.currentIndex()
        suggestion = self.current_analysis.suggestions[index]
        
        preview_text = f"Suggestion: {suggestion['name']}\n\n"
        preview_text += "Folder Structure:\n"
        
        for group_name, folder_path in suggestion["structure"].items():
            if group_name in self.current_analysis.file_groups:
                file_count = len(self.current_analysis.file_groups[group_name])
                preview_text += f"  📁 {folder_path}/\n"
                preview_text += f"     ({file_count} files)\n"
        
        QMessageBox.information(self, "Structure Preview", preview_text)
    
    def apply_suggestion(self):
        if not self.current_analysis:
            QMessageBox.warning(self, "No Analysis", "Please analyze files first.")
            return
        
        index = self.suggestion_combo.currentIndex()
        suggestion = self.current_analysis.suggestions[index]
        
        reply = QMessageBox.question(
            self, "Apply Organization",
            f"Apply '{suggestion['name']}'?\n\nThis will create folders and move files.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                result = self.current_analysis.apply_structure(index)
                QMessageBox.information(
                    self, "Success",
                    f"Created {len(result['created_folders'])} folder(s)\n"
                    f"Moved {result['moved_files']} file(s)"
                )
                self.analyze_files()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to apply structure: {str(e)}")
    
    def analysis_finished(self):
        if self.current_analysis:
            count = sum(len(files) for files in self.current_analysis.file_groups.values())
            self.status_label.setText(f"Analysis complete: {count} files in {len(self.current_analysis.file_groups)} groups")
        else:
            self.status_label.setText("Analysis failed")
    
    def handle_error(self, error):
        QMessageBox.critical(self, "Error", f"Analysis failed: {error}")
        self.status_label.setText("Error during analysis")
