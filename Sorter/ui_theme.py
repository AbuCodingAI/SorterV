from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QStyleFactory


def apply_modern_theme(app):
    """Apply a modern, glossy dark theme with clean colors"""
    
    dark_stylesheet = """
    QMainWindow {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    
    QWidget {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    
    QLineEdit {
        background-color: #2d2d2d;
        color: #ffffff;
        border: 2px solid #404040;
        border-radius: 6px;
        padding: 8px;
        font-size: 12px;
        selection-background-color: #0d7377;
    }
    
    QLineEdit:focus {
        border: 2px solid #0d7377;
        background-color: #333333;
    }
    
    QPushButton {
        background-color: #0d7377;
        color: #ffffff;
        border: none;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: bold;
        font-size: 12px;
    }
    
    QPushButton:hover {
        background-color: #14919b;
    }
    
    QPushButton:pressed {
        background-color: #0a5a61;
    }
    
    QListWidget {
        background-color: #2d2d2d;
        color: #ffffff;
        border: 2px solid #404040;
        border-radius: 6px;
        outline: none;
    }
    
    QListWidget::item {
        padding: 8px;
        border-radius: 4px;
    }
    
    QListWidget::item:hover {
        background-color: #3d3d3d;
    }
    
    QListWidget::item:selected {
        background-color: #0d7377;
    }
    
    QLabel {
        color: #ffffff;
        font-size: 12px;
    }
    
    QComboBox {
        background-color: #2d2d2d;
        color: #ffffff;
        border: 2px solid #404040;
        border-radius: 6px;
        padding: 6px;
        font-size: 12px;
    }
    
    QComboBox:focus {
        border: 2px solid #0d7377;
    }
    
    QComboBox::drop-down {
        border: none;
    }
    
    QComboBox QAbstractItemView {
        background-color: #2d2d2d;
        color: #ffffff;
        selection-background-color: #0d7377;
        border: 2px solid #404040;
    }
    
    QCheckBox {
        color: #ffffff;
        spacing: 8px;
        font-size: 12px;
    }
    
    QCheckBox::indicator {
        width: 18px;
        height: 18px;
        border-radius: 3px;
        border: 2px solid #404040;
        background-color: #2d2d2d;
    }
    
    QCheckBox::indicator:hover {
        border: 2px solid #0d7377;
    }
    
    QCheckBox::indicator:checked {
        background-color: #0d7377;
        border: 2px solid #0d7377;
    }
    
    QDialog {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    
    QMessageBox {
        background-color: #1a1a1a;
    }
    
    QMessageBox QLabel {
        color: #ffffff;
    }
    
    QMessageBox QPushButton {
        min-width: 60px;
    }
    
    QScrollBar:vertical {
        background-color: #2d2d2d;
        width: 12px;
        border-radius: 6px;
    }
    
    QScrollBar::handle:vertical {
        background-color: #0d7377;
        border-radius: 6px;
        min-height: 20px;
    }
    
    QScrollBar::handle:vertical:hover {
        background-color: #14919b;
    }
    
    QScrollBar:horizontal {
        background-color: #2d2d2d;
        height: 12px;
        border-radius: 6px;
    }
    
    QScrollBar::handle:horizontal {
        background-color: #0d7377;
        border-radius: 6px;
        min-width: 20px;
    }
    
    QScrollBar::handle:horizontal:hover {
        background-color: #14919b;
    }
    """
    
    app.setStyle(QStyleFactory.create('Fusion'))
    app.setStyleSheet(dark_stylesheet)
