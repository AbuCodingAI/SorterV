"""
TimeSort GUI - Find files not accessed in X days
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QPushButton,
    QListWidget, QListWidgetItem, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont
import os
from time_sort import TimeSort


class TimeSortScanner(QThread):
    """Background thread for scanning files"""
    results_found = pyqtSignal(list)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, folder_path, days):
        super().__init__()
        self.folder_path = folder_path
        self.days = days
    
    def run(self):
        try:
            results = TimeSort(self.folder_path, self.days)
            details = results.get_details()
            self.results_found.emit(details)
        except Exception as e:
            self.error_occurred.emit(str(e))


class TimeSortWidget(QWidget):
    """TimeSort GUI Widget"""
    
    def __init__(self):
        super().__init__()
        self.selected_files = set()
        self.current_results = []
        self.scanner_thread = None
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Header
        header_label = QLabel("TimeSort - Find Old Files")
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
        
        layout.addLayout(folder_layout)
        
        # Days selection
        days_layout = QHBoxLayout()
        days_label = QLabel("Files not accessed in:")
        days_layout.addWidget(days_label)
        
        self.days_spinbox = QSpinBox()
        self.days_spinbox.setMinimum(1)
        self.days_spinbox.setMaximum(3650)
        self.days_spinbox.setValue(30)
        self.days_spinbox.setMinimumHeight(35)
        self.days_spinbox.setMinimumWidth(80)
        days_layout.addWidget(self.days_spinbox)
        
        days_unit = QLabel("days")
        days_layout.addWidget(days_unit)
        
        scan_btn = QPushButton("🔍 Scan")
        scan_btn.clicked.connect(self.scan_files)
        scan_btn.setMinimumHeight(35)
        days_layout.addWidget(scan_btn)
        
        days_layout.addStretch()
        layout.addLayout(days_layout)
        
        # Results
        results_label = QLabel("Results:")
        layout.addWidget(results_label)
        
        self.results_list = QListWidget()
        self.results_list.itemClicked.connect(self.on_item_clicked)
        layout.addWidget(self.results_list)
        
        # Status
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        delete_btn = QPushButton("🗑️ Delete Selected")
        delete_btn.clicked.connect(lambda: self.perform_action("delete"))
        action_layout.addWidget(delete_btn)
        
        copy_btn = QPushButton("📋 Copy Selected")
        copy_btn.clicked.connect(lambda: self.perform_action("copy"))
        action_layout.addWidget(copy_btn)
        
        move_btn = QPushButton("📦 Move Selected")
        move_btn.clicked.connect(lambda: self.perform_action("move"))
        action_layout.addWidget(move_btn)
        
        clear_btn = QPushButton("Clear Selection")
        clear_btn.clicked.connect(self.clear_selection)
        action_layout.addWidget(clear_btn)
        
        layout.addLayout(action_layout)
        
        self.setLayout(layout)
    
    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder to Scan")
        if folder:
            self.folder_label.setText(f"📂 {folder}")
            self.status_label.setText("Folder selected. Set days and scan.")
    
    def scan_files(self):
        folder = self.folder_label.text()
        if folder == "No folder selected" or not folder.startswith("📂"):
            QMessageBox.warning(self, "No Folder", "Please select a folder first.")
            return
        
        folder_path = folder.replace("📂 ", "")
        days = self.days_spinbox.value()
        
        self.status_label.setText("Scanning...")
        self.results_list.clear()
        self.selected_files.clear()
        
        self.scanner_thread = TimeSortScanner(folder_path, days)
        self.scanner_thread.results_found.connect(self.display_results)
        self.scanner_thread.error_occurred.connect(self.handle_error)
        self.scanner_thread.finished.connect(self.scan_finished)
        self.scanner_thread.start()
    
    def display_results(self, details):
        self.current_results = details
        for item in details:
            display_text = f"{os.path.basename(item['path'])} ({item['days_ago']} days ago)"
            list_item = QListWidgetItem(display_text)
            list_item.setData(Qt.ItemDataRole.UserRole, item['path'])
            list_item.setCheckState(Qt.CheckState.Unchecked)
            self.results_list.addItem(list_item)
    
    def scan_finished(self):
        count = len(self.current_results)
        self.status_label.setText(f"Found {count} item(s)")
    
    def handle_error(self, error):
        QMessageBox.critical(self, "Error", f"Scan failed: {error}")
        self.status_label.setText("Error during scan")
    
    def on_item_clicked(self, item):
        if item.checkState() == Qt.CheckState.Unchecked:
            item.setCheckState(Qt.CheckState.Checked)
            self.selected_files.add(item.data(Qt.ItemDataRole.UserRole))
        else:
            item.setCheckState(Qt.CheckState.Unchecked)
            self.selected_files.discard(item.data(Qt.ItemDataRole.UserRole))
    
    def clear_selection(self):
        self.selected_files.clear()
        for i in range(self.results_list.count()):
            self.results_list.item(i).setCheckState(Qt.CheckState.Unchecked)
    
    def perform_action(self, action):
        if not self.selected_files:
            QMessageBox.warning(self, "No Selection", "Please select files first.")
            return
        
        if action == "delete":
            self.delete_files()
        elif action == "copy":
            self.copy_files()
        elif action == "move":
            self.move_files()
    
    def delete_files(self):
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Delete {len(self.selected_files)} file(s)? This cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            import shutil
            deleted = 0
            for file_path in self.selected_files:
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                    deleted += 1
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"Failed to delete {file_path}: {str(e)}")
            
            QMessageBox.information(self, "Success", f"Deleted {deleted} item(s)")
            self.scan_files()
    
    def copy_files(self):
        dest_folder = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
        if not dest_folder:
            return
        
        import shutil
        copied = 0
        for file_path in self.selected_files:
            try:
                dest_path = os.path.join(dest_folder, os.path.basename(file_path))
                if os.path.isfile(file_path):
                    shutil.copy2(file_path, dest_path)
                elif os.path.isdir(file_path):
                    shutil.copytree(file_path, dest_path)
                copied += 1
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to copy {file_path}: {str(e)}")
        
        QMessageBox.information(self, "Success", f"Copied {copied} item(s)")
    
    def move_files(self):
        dest_folder = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
        if not dest_folder:
            return
        
        import shutil
        moved = 0
        for file_path in self.selected_files:
            try:
                dest_path = os.path.join(dest_folder, os.path.basename(file_path))
                shutil.move(file_path, dest_path)
                moved += 1
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to move {file_path}: {str(e)}")
        
        QMessageBox.information(self, "Success", f"Moved {moved} item(s) to {dest_folder}")
        self.scan_files()
