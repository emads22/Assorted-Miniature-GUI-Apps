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

        self.setWindowTitle("File Compressor")
        # Set fixed window size
        self.setFixedSize(600, 200)

        # Set theme (custom style sheet)
        self.setStyleSheet("""
            background-color: #0F1035;
            color: #fff;
            font-size: 16px;
            font-weight: bold;
        """)

        # set the values of the respected archive files and destination paths
        self.files_list = []
        self.filenames_str = " No file(s) selected yet"
        self.destination_path = " No destination folder selected yet"

        # First layout
        files_label = QLabel("Select file(s): ")
        # link it to the class properties in order to be accessed everywhere by the instance of this class
        self.files_input = QLineEdit()
        self.files_input.setPlaceholderText(
            self.filenames_str)
        # Set this input field to read-only
        self.files_input.setReadOnly(True)
        files_browse_button = QPushButton("Browse")
        files_browse_button.setStyleSheet(
            "background-color: #365486;")
        files_browse_button.clicked.connect(self.browse_files)

        files_layout = QHBoxLayout()
        files_layout.addWidget(files_label)
        files_layout.addWidget(self.files_input)
        files_layout.addWidget(files_browse_button)

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
        compress_button = QPushButton("Compress")
        compress_button.setStyleSheet(
            "background-color: #365486;")
        # Connect compress_button clicked signal to a function
        compress_button.clicked.connect(self.on_compress_button_clicked)
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
        third_layout.addWidget(compress_button)
        third_layout.addWidget(clear_button)
        third_layout.addWidget(self.result_label)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(files_layout)
        main_layout.addLayout(destination_layout)
        main_layout.addLayout(third_layout)

        # Add padding to main layout
        main_layout.setContentsMargins(
            30, 30, 30, 20)  # left, top, right, bottom

        # Central widget or container widget cz we cant pass a layout to setCentralWidget()
        container_widget = QWidget()
        container_widget.setLayout(main_layout)
        self.setCentralWidget(container_widget)

    def on_compress_button_clicked(self):
        # Check if input fields are empty means nothing was selected
        if self.files_input.text().strip() == "" or self.destination_input.text().strip() == "":
            # Show QMessageBox if input fields are empty
            QMessageBox.warning(
                self, "Warning", "Please make sure to select at least one file and specify a destination directory.")
        else:
            # call the archive_files() function with the list of files (path) to create archived zip file
            self.archive_files(self.files_list, self.destination_path)

    def browse_files(self):
        self.files_list, _ = QFileDialog.getOpenFileNames(
            self, "Select Files", "", "All Files (*);;Text Files (*.txt)")
        if self.files_list:
            # convert list of file paths to a list of file names
            self.files_list = [file.split('/')[-1] for file in self.files_list]
            # convert this list of file names to a str separated by ', ' to display it in the input
            self.filenames_str = ", ".join(self.files_list)
            self.files_input.setText(self.filenames_str)

    def browse_destination_folder(self):
        folder_dialog = QFileDialog(self)
        folder_dialog.setFileMode(QFileDialog.FileMode.Directory)
        self.destination_path = folder_dialog.getExistingDirectory(
            self, "Select Destination Folder")
        if self.destination_path:
            # extract the name of folder only instead of full path
            # folder_name = self.destination_path.split('/')[-1]
            self.destination_input.setText(self.destination_path)

    def clear_fields(self):
        self.files_input.clear()
        self.destination_input.clear()
        self.result_label.clear()

    def archive_files(self, files_to_archive, destination_path):
        # Create a Path object for the destination path
        destination_path_object = Path(destination_path)
        # Ensure the destination directory exists, if not, create it
        destination_path_object.mkdir(parents=True, exist_ok=True)
        
        # Format the current datetime object as a string
        current_date = datetime.now().strftime("%d-%m-%Y")
        # add to this path object the name 'archive' wth the current date then extension '.zip' to rename it
        archive_file_path = destination_path_object / f'archive_[{current_date}].zip'

        try:
            # Create a new zip file
            with zipfile.ZipFile(archive_file_path, 'w') as zipf:
                # Add each file to the zip archive
                for filepath in files_to_archive:
                    # Convert path string to Path object to check if exists
                    if Path(filepath).exists():
                        # this function accepts only string
                        zipf.write(filepath)
                    else:
                        print(f"File not found: {filepath}")
            # add success message to the result label
            # self.result_label.setText(" Files archived successfully.")
            # display success message
            QMessageBox.information(
                self, "Success", "Files archived successfully.")
            self.clear_fields()

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
