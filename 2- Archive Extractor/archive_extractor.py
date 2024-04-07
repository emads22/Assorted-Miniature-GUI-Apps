import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QSizePolicy, QMessageBox, QFileDialog)
import zipfile
from pathlib import Path
from datetime import datetime


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Archive Extractor")
        # Set fixed window size
        self.setFixedSize(600, 200)

        # Set theme (custom style sheet)
        self.setStyleSheet("""
            background-color: #0F1035;
            color: #fff;
            font-size: 16px;
            font-weight: bold;
        """)

        # set the values of the respected archive file and destination paths
        self.archive_path = " No archive file selected yet"
        self.destination_path = " No destination folder selected yet"

        # First layout
        archive_label = QLabel("Select archive file: ")
        # link it to the class properties in order to be accessed everywhere by the instance of this class
        self.archive_input = QLineEdit()
        self.archive_input.setPlaceholderText(
            self.archive_path)
        # Set this input field to read-only
        self.archive_input.setReadOnly(True)
        file_browse_button = QPushButton("Browse")
        file_browse_button.setStyleSheet(
            "background-color: #365486;")
        file_browse_button.clicked.connect(self.browse_archive_file)

        archive_layout = QHBoxLayout()
        archive_layout.addWidget(archive_label)
        archive_layout.addWidget(self.archive_input)
        archive_layout.addWidget(file_browse_button)

        # Second layout
        destination_label = QLabel("Select destination: ")
        self.destination_input = QLineEdit()
        self.destination_input.setPlaceholderText(
            self.destination_path)
        # Set this input field to read-only
        self.destination_input.setReadOnly(True)
        folder_browse_button = QPushButton("Browse")
        folder_browse_button.setStyleSheet(
            "background-color: #365486;")
        folder_browse_button.clicked.connect(self.browse_destination_folder)

        destination_layout = QHBoxLayout()
        destination_layout.addWidget(destination_label)
        destination_layout.addWidget(self.destination_input)
        destination_layout.addWidget(folder_browse_button)

        # Third layout
        extract_button = QPushButton("Extract")
        extract_button.setStyleSheet(
            "background-color: #365486;")
        # Connect extract_button clicked signal to a function
        extract_button.clicked.connect(self.on_extract_button_clicked)
        clear_button = QPushButton("Clear")
        clear_button.setStyleSheet(
            "background-color: #365486;")
        # Connect compress_button clicked signal to a function
        clear_button.clicked.connect(self.clear_fields)
        self.result_label = QLabel("")
        # make result_label take up auto space
        self.result_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        third_layout = QHBoxLayout()
        third_layout.addWidget(extract_button)
        third_layout.addWidget(clear_button)
        third_layout.addWidget(self.result_label)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(archive_layout)
        main_layout.addLayout(destination_layout)
        main_layout.addLayout(third_layout)

        # Add padding to main layout
        main_layout.setContentsMargins(
            30, 30, 30, 20)  # left, top, right, bottom

        # Central widget or container widget cz we cant pass a layout to setCentralWidget()
        container_widget = QWidget()
        container_widget.setLayout(main_layout)
        self.setCentralWidget(container_widget)

    def on_extract_button_clicked(self):
        # Check if input fields are empty means nothing was selected
        if self.archive_input.text().strip() == "" or self.destination_input.text().strip() == "":
            # Show QMessageBox if input fields are empty
            QMessageBox.warning(
                self, "Warning", "Please make sure to select both an archive file and a destination directory.")
        else:
            # skip this function and continue if input fields are not empty
            self.extract_file(self.archive_path, self.destination_path)

    def browse_archive_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        # Filter only ZIP files to be selected
        self.archive_path, _ = file_dialog.getOpenFileName(
            self, "Select Archive", "", "ZIP Files (*.zip)")
        if self.archive_path:
            # set the path in the respective input text
            self.archive_input.setText(self.archive_path)

    def browse_destination_folder(self):
        folder_dialog = QFileDialog(self)
        folder_dialog.setFileMode(QFileDialog.FileMode.Directory)
        self.destination_path = folder_dialog.getExistingDirectory(
            self, "Select Destination Folder")
        if self.destination_path:
            # set the path in the respective input text
            self.destination_input.setText(self.destination_path)

    def clear_fields(self):
        self.archive_input.clear()
        self.destination_input.clear()
        self.result_label.clear()

    def extract_file(self, filepath, destination_path):
        # Convert file path string to Path object
        filepath_object = Path(filepath)

        # Format the current datetime object as a string
        current_date = datetime.now().strftime("%d-%m-%Y")
        # Create a Path object for the destination path and concatenate with 'extracted_files' and the current date
        extracted_files_path = Path(
            destination_path) / f'extracted_files_[{current_date}]'

        try:
            # Open an existing zip file
            with zipfile.ZipFile(filepath_object, 'r') as zipf:
                # Extract all files from the zip archive
                zipf.extractall(extracted_files_path)
            # add success message to the result label
            # self.result_label.setText(" Files extracted successfully.")
            # display success message
            QMessageBox.information(
                self, "Success", "Files extracted successfully.")
            self.clear_fields()

        except FileNotFoundError:
            QMessageBox.warning(
                self, "Warning", f'File not found:  "{filepath}"')
        except Exception as e:
            QMessageBox.warning(
                self, "Warning", f"Error archiving files: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # using sys.exit(app.exec()) instead of app.exec() below ensures the PyQt application closes cleanly
    # and exits the Python interpreter when the app finishes executing, allowing closure from the console.
    sys.exit(app.exec())
