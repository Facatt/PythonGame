import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog, QVBoxLayout, QHBoxLayout, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class ImageBrowser(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Image Browser and Renamer')
        self.setGeometry(100, 100, 800, 600)

        # Layouts
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Image Label
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.image_label)

        # Buttons
        buttons_layout = QHBoxLayout()
        main_layout.addLayout(buttons_layout)

        # Open Folder Button
        self.open_folder_btn = QPushButton('Open Folder')
        self.open_folder_btn.clicked.connect(self.open_folder)
        buttons_layout.addWidget(self.open_folder_btn)

        # Previous Button
        self.prev_btn = QPushButton('Previous')
        self.prev_btn.clicked.connect(self.prev_image)
        buttons_layout.addWidget(self.prev_btn)

        # Next Button
        self.next_btn = QPushButton('Next')
        self.next_btn.clicked.connect(self.next_image)
        buttons_layout.addWidget(self.next_btn)

        # Rename Section
        rename_layout = QVBoxLayout()
        main_layout.addLayout(rename_layout)

        # Input Boxes
        self.input_boxes = {}
        labels = ["整齐性", "一致性", "量多/少", "装饰"]
        for label in labels:
            layout = QHBoxLayout()
            layout.addWidget(QLabel(label))
            line_edit = QLineEdit()
            layout.addWidget(line_edit)
            rename_layout.addLayout(layout)
            self.input_boxes[label] = line_edit

        # Rename Button
        self.rename_btn = QPushButton('Rename Image')
        self.rename_btn.clicked.connect(self.rename_image)
        main_layout.addWidget(self.rename_btn)

        # Revert Current Rename Button
        self.revert_current_btn = QPushButton('Revert Current Rename')
        self.revert_current_btn.clicked.connect(self.revert_current)
        main_layout.addWidget(self.revert_current_btn)

        # Revert All Rename Button
        self.revert_all_btn = QPushButton('Revert All Rename')
        self.revert_all_btn.clicked.connect(self.revert_all)
        main_layout.addWidget(self.revert_all_btn)

        self.image_list = []
        self.current_image_index = 0
        self.original_names = []

    def open_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Open Folder')
        if folder_path:
            self.image_list = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
            self.original_names = [self.get_original_name(f) for f in self.image_list]  # Store original names
            if self.image_list:
                self.current_image_index = 0
                self.show_image()

    def get_original_name(self, file_path):
        base_name = os.path.basename(file_path)
        parts = base_name.split('_')
        original_name = parts[0]
        for i in range(1, len(parts)):
            if not parts[i].isdigit() or not parts[i].lower() in ['true', 'false']:
                original_name += '_' + parts[i]
                break
        return original_name

    def show_image(self):
        if self.image_list:
            pixmap = QPixmap(self.image_list[self.current_image_index])
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))

    def prev_image(self):
        if self.image_list and self.current_image_index > 0:
            self.current_image_index -= 1
            self.show_image()
            self.clear_inputs()

    def next_image(self):
        if self.image_list and self.current_image_index < len(self.image_list) - 1:
            self.current_image_index += 1
            self.show_image()
            self.clear_inputs()

    def clear_inputs(self):
        for line_edit in self.input_boxes.values():
            line_edit.clear()

    def rename_image(self):
        current_image_path = self.image_list[self.current_image_index]
        base_name = self.original_names[self.current_image_index]
        file_name, file_ext = os.path.splitext(base_name)

        new_name_parts = [file_name]
        for key, line_edit in self.input_boxes.items():
            value = line_edit.text()
            if value:  # Only add to the name if the input is not empty
                new_name_parts.append(str(value))  # Convert True to string
        new_name = '_'.join(new_name_parts) + file_ext

        new_image_path = os.path.join(os.path.dirname(current_image_path), new_name)
        os.rename(current_image_path, new_image_path)
        self.image_list[self.current_image_index] = new_image_path  # Update the list with new path
        self.original_names[self.current_image_index] = os.path.basename(new_image_path)  # Update original name

    def revert_current(self):
        if self.image_list and self.current_image_index < len(self.image_list):
            current_image_path = self.image_list[self.current_image_index]
            original_name = self.original_names[self.current_image_index]
            original_path = os.path.join(os.path.dirname(current_image_path), original_name)
            os.rename(current_image_path, original_path)
            self.image_list[self.current_image_index] = original_path  # Update the list with original path

    def revert_all(self):
        for i, original_name in enumerate(self.original_names):
            current_image_path = self.image_list[i]
            original_path = os.path.join(os.path.dirname(current_image_path), original_name)
            os.rename(current_image_path, original_path)
            self.image_list[i] = original_path  # Update the list with original path

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageBrowser()
    ex.show()
    sys.exit(app.exec_())