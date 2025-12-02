import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QListWidget, QListWidgetItem, QFileDialog,
    QMessageBox, QCheckBox, QLabel, QComboBox, QSpinBox, QDialog,
    QTabWidget, QScrollArea
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QIcon, QFont, QColor, QPixmap
from PyQt6.QtCore import QSize
import json
from file_scanner import FileScanner
from ui_theme import apply_modern_theme

# Import SmartSort GUIs if available
try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Smart Sorter'))
    from time_sort_gui import TimeSortWidget
    from smart_sort_gui import SmartSortWidget
    SMARTSORT_AVAILABLE = True
except ImportError:
    SMARTSORT_AVAILABLE = False

class PermissionDialog(QDialog):
    """Permission request dialog"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("File Explorer Access Permission")
        self.setGeometry(200, 200, 600, 400)
        self.setModal(True)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Sorter - File Explorer Access Permission")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Permission request text
        permission_text = QLabel(
            "Sorter needs permission to access your file explorer to:\n\n"
            "✓ Search for files by keyword\n"
            "✓ Find old files by access time\n"
            "✓ Organize files by name patterns\n"
            "✓ Perform file operations (delete, copy, move)\n\n"
            "Privacy Promise:\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "• We will NOT read file contents unless you explicitly ask\n"
            "• We will NOT upload or transmit any data\n"
            "• We will NOT access files outside your selected folder\n"
            "• All operations are local to your machine\n"
            "• This is open-source software - you can verify the code\n\n"
            "If this application is compromised or hacked, we cannot\n"
            "guarantee file safety. Use at your own risk."
        )
        permission_text.setWordWrap(True)
        layout.addWidget(permission_text)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        allow_btn = QPushButton("✓ Allow Access")
        allow_btn.setMinimumHeight(40)
        allow_btn.clicked.connect(self.accept)
        button_layout.addWidget(allow_btn)
        
        deny_btn = QPushButton("✗ Deny Access")
        deny_btn.setMinimumHeight(40)
        deny_btn.clicked.connect(self.reject)
        button_layout.addWidget(deny_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)


class SorterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sorter - File Management Tool")
        self.setGeometry(100, 100, 1000, 700)
        if os.path.exists("assets/icon.png"):
            self.setWindowIcon(QIcon("assets/icon.png"))
        
        self.config = self.load_config()
        self.selected_files = set()
        self.current_results = []
        self.scanner_thread = None
        self.permission_granted = False
        
        # Check for permission
        if not self.check_permission():
            self.show_permission_denied()
            return
        
        self.init_ui()
        apply_modern_theme(self)
    
    def check_permission(self):
        """Check if user has granted file explorer access permission"""
        if self.config.get("file_access_permission_granted"):
            return True
        
        # Show permission dialog
        perm_dialog = PermissionDialog(self)
        if perm_dialog.exec() == QDialog.DialogCode.Accepted:
            self.config["file_access_permission_granted"] = True
            self.save_config()
            self.permission_granted = True
            return True
        
        return False
    
    def show_permission_denied(self):
        """Show message when permission is denied"""
        self.setWindowTitle("Sorter - Permission Denied")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        
        denied_label = QLabel(
            "❌ File Explorer Access Denied\n\n"
            "Sorter requires file explorer access to function.\n"
            "Without this permission, the application cannot:\n\n"
            "• Search for files\n"
            "• Organize files\n"
            "• Perform file operations\n\n"
            "To use Sorter, please restart the application\n"
            "and grant file explorer access permission."
        )
        denied_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        denied_label.setStyleSheet("font-size: 14px; color: #ff6b6b;")
        layout.addWidget(denied_label)
        
        restart_btn = QPushButton("Restart Application")
        restart_btn.clicked.connect(self.restart_app)
        layout.addWidget(restart_btn)
        
        central_widget.setLayout(layout)
        
    def restart_app(self):
        """Restart the application"""
        import subprocess
        subprocess.Popen([sys.executable] + sys.argv)
        sys.exit()
    
    def init_ui(self):
        if not self.permission_granted:
            return
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        
        # Create tabs
        self.tabs = QTabWidget()
        
        # Tab 1: Keyword Sorter
        keyword_widget = self.create_keyword_sorter_tab()
        self.tabs.addTab(keyword_widget, "🔍 Keyword Sorter")
        
        # Tab 2: TimeSort (if available)
        if SMARTSORT_AVAILABLE:
            self.time_sort_widget = TimeSortWidget()
            self.tabs.addTab(self.time_sort_widget, "⏰ TimeSort")
        
        # Tab 3: SmartSort (if available)
        if SMARTSORT_AVAILABLE:
            self.smart_sort_widget = SmartSortWidget()
            self.tabs.addTab(self.smart_sort_widget, "🧠 SmartSort")
        
        main_layout.addWidget(self.tabs)
        central_widget.setLayout(main_layout)
    
    def create_keyword_sorter_tab(self):
        """Create the keyword sorter tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Header section
        header_layout = QHBoxLayout()
        
        folder_btn = QPushButton("📁 Select Folder")
        folder_btn.clicked.connect(self.select_folder)
        folder_btn.setMinimumHeight(40)
        header_layout.addWidget(folder_btn)
        
        self.folder_label = QLabel("No folder selected")
        self.folder_label.setStyleSheet("color: #888; font-style: italic;")
        header_layout.addWidget(self.folder_label)
        
        layout.addLayout(header_layout)
        
        # Search section
        search_layout = QHBoxLayout()
        
        search_label = QLabel("Keyword:")
        search_layout.addWidget(search_label)
        
        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText("Enter keyword (e.g., backup)")
        self.keyword_input.setMinimumHeight(35)
        self.keyword_input.returnPressed.connect(self.search_files)
        search_layout.addWidget(self.keyword_input)
        
        search_btn = QPushButton("🔍 Search")
        search_btn.clicked.connect(self.search_files)
        search_btn.setMinimumHeight(35)
        search_layout.addWidget(search_btn)
        
        settings_btn = QPushButton("⚙️ Settings")
        settings_btn.clicked.connect(self.open_settings)
        settings_btn.setMinimumHeight(35)
        search_layout.addWidget(settings_btn)
        
        layout.addLayout(search_layout)
        
        # Results section
        results_label = QLabel("Results:")
        layout.addWidget(results_label)
        
        self.results_list = QListWidget()
        self.results_list.itemClicked.connect(self.on_item_clicked)
        layout.addWidget(self.results_list)
        
        # Status bar
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
        
        folder_btn = QPushButton("📦 Move to Folder")
        folder_btn.clicked.connect(lambda: self.perform_action("folder"))
        action_layout.addWidget(folder_btn)
        
        clear_btn = QPushButton("Clear Selection")
        clear_btn.clicked.connect(self.clear_selection)
        action_layout.addWidget(clear_btn)
        
        layout.addLayout(action_layout)
        
        widget.setLayout(layout)
        return widget
        
    def select_folder(self):
        if not self.permission_granted:
            QMessageBox.warning(self, "Permission Denied", "File explorer access was not granted.")
            return
        
        folder = QFileDialog.getExistingDirectory(self, "Select Folder to Search")
        if folder:
            self.config["last_folder"] = folder
            self.save_config()
            self.folder_label.setText(f"📂 {folder}")
            self.status_label.setText("Folder selected. Enter keyword and search.")
    
    def search_files(self):
        if not self.config.get("last_folder"):
            QMessageBox.warning(self, "No Folder", "Please select a folder first.")
            return
        
        keyword = self.keyword_input.text().strip()
        if not keyword:
            QMessageBox.warning(self, "No Keyword", "Please enter a keyword.")
            return
        
        self.status_label.setText("Searching...")
        self.results_list.clear()
        self.selected_files.clear()
        
        self.scanner_thread = FileScanner(
            self.config["last_folder"],
            keyword,
            self.config.get("case_sensitive", False),
            self.config.get("include_plural", True)
        )
        self.scanner_thread.results_found.connect(self.display_results)
        self.scanner_thread.finished.connect(self.search_finished)
        self.scanner_thread.start()
    
    def display_results(self, results):
        self.current_results = results
        for file_path in results:
            item = QListWidgetItem(file_path)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.results_list.addItem(item)
    
    def search_finished(self):
        count = len(self.current_results)
        self.status_label.setText(f"Found {count} result(s)")
    
    def on_item_clicked(self, item):
        if item.checkState() == Qt.CheckState.Unchecked:
            item.setCheckState(Qt.CheckState.Checked)
            self.selected_files.add(item.text())
        else:
            item.setCheckState(Qt.CheckState.Unchecked)
            self.selected_files.discard(item.text())
    
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
        elif action == "folder":
            self.move_to_folder()
    
    def delete_files(self):
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Delete {len(self.selected_files)} file(s)? This cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            deleted = 0
            for file_path in self.selected_files:
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        import shutil
                        shutil.rmtree(file_path)
                    deleted += 1
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"Failed to delete {file_path}: {str(e)}")
            
            QMessageBox.information(self, "Success", f"Deleted {deleted} item(s)")
            self.search_files()
    
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
    
    def move_to_folder(self):
        dest_folder = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
        if not dest_folder:
            return
        
        folder_name = QFileDialog.getSaveFileName(
            self, "Create New Folder", dest_folder, "Folder"
        )[0]
        
        if not folder_name:
            folder_name = os.path.join(dest_folder, "Sorted_Files")
        
        os.makedirs(folder_name, exist_ok=True)
        
        import shutil
        moved = 0
        for file_path in self.selected_files:
            try:
                dest_path = os.path.join(folder_name, os.path.basename(file_path))
                shutil.move(file_path, dest_path)
                moved += 1
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to move {file_path}: {str(e)}")
        
        QMessageBox.information(self, "Success", f"Moved {moved} item(s) to {folder_name}")
        self.search_files()
    
    def open_settings(self):
        settings_dialog = SettingsDialog(self, self.config)
        if settings_dialog.exec() == QDialog.DialogCode.Accepted:
            self.config = settings_dialog.get_config()
            self.save_config()
    
    def load_config(self):
        config_path = "config.json"
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                return json.load(f)
        return {
            "last_folder": "",
            "case_sensitive": False,
            "include_plural": True,
            "theme": "dark"
        }
    
    def save_config(self):
        with open("config.json", "w") as f:
            json.dump(self.config, f, indent=2)


class SettingsDialog(QDialog):
    def __init__(self, parent, config):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setGeometry(200, 200, 400, 300)
        self.config = config.copy()
        
        layout = QVBoxLayout()
        
        # Case sensitive
        self.case_sensitive_check = QCheckBox("Case Sensitive Search")
        self.case_sensitive_check.setChecked(self.config.get("case_sensitive", False))
        layout.addWidget(self.case_sensitive_check)
        
        # Include plural
        self.include_plural_check = QCheckBox("Include Plural Forms (e.g., backup → backups)")
        self.include_plural_check.setChecked(self.config.get("include_plural", True))
        layout.addWidget(self.include_plural_check)
        
        # Theme
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("Theme:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light"])
        self.theme_combo.setCurrentText(self.config.get("theme", "Dark").capitalize())
        theme_layout.addWidget(self.theme_combo)
        layout.addLayout(theme_layout)
        
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def get_config(self):
        self.config["case_sensitive"] = self.case_sensitive_check.isChecked()
        self.config["include_plural"] = self.include_plural_check.isChecked()
        self.config["theme"] = self.theme_combo.currentText().lower()
        return self.config


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SorterApp()
    window.show()
    sys.exit(app.exec())
