import os
import shutil
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, 
                              QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, 
                              QFileDialog, QMessageBox, QLabel, QFrame)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon

class ModernFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            ModernFrame {
                background-color: #ffffff;
                border-radius: 10px;
                border: 1px solid #e0e0e0;
            }
        """)

class FileOrganizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Organizer")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QLineEdit {
                padding: 8px;
                border-radius: 5px;
                border: 1px solid #e0e0e0;
                background-color: white;
            }
            QTextEdit {
                border-radius: 5px;
                border: 1px solid #e0e0e0;
                background-color: white;
                padding: 8px;
            }
        """)

        self.extension_mapping = {
            'DOCUMENTS': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt'],
            'IMAGES': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'],
            'AUDIO': ['.mp3', '.wav', '.flac', '.m4a', '.aac'],
            'VIDEO': ['.mp4', '.avi', '.mkv', '.mov', '.wmv'],
            'ARCHIVES': ['.zip', '.rar', '.7z', '.tar', '.gz'],
            'EXE': ['.exe', '.msi'],
            'PROGRAMMING': ['.py', '.java', '.cpp', '.c', '.html', '.css', '.js'],
            'OTHER': []
        }

        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        title_label = QLabel("File Organizer")
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        dir_frame = ModernFrame()
        dir_layout = QVBoxLayout(dir_frame)
        
        dir_label = QLabel("Select folder to sort:")
        dir_label.setFont(QFont("Arial", 10))
        dir_layout.addWidget(dir_label)

        dir_input_layout = QHBoxLayout()
        self.dir_entry = QLineEdit()
        self.browse_btn = QPushButton("Browse")
        self.browse_btn.clicked.connect(self.browse_directory)
        
        dir_input_layout.addWidget(self.dir_entry)
        dir_input_layout.addWidget(self.browse_btn)
        dir_layout.addLayout(dir_input_layout)
        
        main_layout.addWidget(dir_frame)

        self.organize_btn = QPushButton("Sort Files")
        self.organize_btn.setFixedHeight(40)
        self.organize_btn.clicked.connect(self.organize_files)
        main_layout.addWidget(self.organize_btn)

        status_frame = ModernFrame()
        status_layout = QVBoxLayout(status_frame)
        
        status_label = QLabel("Status:")
        status_label.setFont(QFont("Arial", 10))
        status_layout.addWidget(status_label)

        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        status_layout.addWidget(self.status_text)
        
        main_layout.addWidget(status_frame)

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select folder")
        if directory:
            self.dir_entry.setText(directory)

    def get_all_files(self, directory):
        all_files = []
        for root, dirs, files in os.walk(directory):
            if any(category in root.split(os.path.sep) for category in self.extension_mapping.keys()):
                continue
            for file in files:
                all_files.append(os.path.join(root, file))
        return all_files

    def organize_files(self):
        directory = self.dir_entry.text()
        if not directory:
            QMessageBox.critical(self, "Error", "Please select a folder to sort!")
            return
            
        self.status_text.clear()
        self.add_status("Starting file sorting...")
        
        try:
            for category in self.extension_mapping.keys():
                category_path = os.path.join(directory, category)
                if not os.path.exists(category_path):
                    os.makedirs(category_path)
                    self.add_status(f"Created folder: {category}")
            
            all_files = self.get_all_files(directory)
            files_moved = 0
            
            for file_path in all_files:
                filename = os.path.basename(file_path)
                _, extension = os.path.splitext(filename)
                extension = extension.lower()
                
                target_category = 'OTHER'
                for category, extensions in self.extension_mapping.items():
                    if extension in extensions:
                        target_category = category
                        break
                
                target_path = os.path.join(directory, target_category, filename)
                
                if os.path.exists(target_path):
                    base, ext = os.path.splitext(filename)
                    counter = 1
                    while os.path.exists(target_path):
                        new_filename = f"{base}_{counter}{ext}"
                        target_path = os.path.join(directory, target_category, new_filename)
                        counter += 1
                
                shutil.move(file_path, target_path)
                files_moved += 1
                self.add_status(f"Moved: {filename} -> {target_category}")
            
            for root, dirs, files in os.walk(directory, topdown=False):
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    if not os.listdir(dir_path) and dir_name not in self.extension_mapping:
                        os.rmdir(dir_path)
                        self.add_status(f"Removed empty folder: {dir_path}")
            
            self.add_status(f"\nCompleted! Sorted {files_moved} files.")
            QMessageBox.information(self, "Success", f"Sorted {files_moved} files!")
            
        except Exception as e:
            self.add_status(f"\nERROR: {str(e)}")
            QMessageBox.critical(self, "Error", f"An error occurred while sorting: {str(e)}")

    def add_status(self, message):
        self.status_text.append(message)
        self.status_text.verticalScrollBar().setValue(
            self.status_text.verticalScrollBar().maximum()
        )
        QApplication.processEvents()

if __name__ == "__main__":
    app = QApplication([])
    window = FileOrganizer()
    window.show()
    app.exec()
