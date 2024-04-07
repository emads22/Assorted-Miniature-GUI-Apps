
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QSizePolicy, QMessageBox)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Meter Converter")
        # Set fixed window size
        self.setFixedSize(400, 200)

        # Set theme (custom style sheet)
        self.setStyleSheet("""
            background-color: #344955;
            color: #fff;
            font-size: 16px;
            font-weight: bold;
        """)

        # set the respected values of feet and inches
        self.feet_value = " 0 "
        self.inches_value = " 0 "
        self.calculation = None

        # First layout
        feet_label = QLabel('Enter "feet" value: ')
        self.feet_input = QLineEdit()
        # link it to the class properties in order to be accessed everywhere by the instance of this class
        self.feet_input.setPlaceholderText(self.feet_value)

        first_layout = QHBoxLayout()
        first_layout.addWidget(feet_label)
        first_layout.addWidget(self.feet_input)

        # Second layout
        inches_label = QLabel('Enter "inches" value: ')
        self.inches_input = QLineEdit()
        self.inches_input.setPlaceholderText(self.inches_value)

        second_layout = QHBoxLayout()
        second_layout.addWidget(inches_label)
        second_layout.addWidget(self.inches_input)

        # Third layout
        convert_button = QPushButton("Convert")
        convert_button.setStyleSheet(
            "background-color: #FF5733;")  # or #070F2B
        # Connect convert_button clicked signal to a function
        convert_button.clicked.connect(self.on_convert_button_clicked)
        clear_button = QPushButton("Clear")
        clear_button.setStyleSheet(
            "background-color: #FF5733;")
        # Connect compress_button clicked signal to a function
        clear_button.clicked.connect(self.clear_fields)
        self.result_label = QLabel("")
        self.result_label.setStyleSheet("color: #fff;")
        # make result_label take up auto space
        self.result_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        third_layout = QHBoxLayout()
        third_layout.addWidget(convert_button)
        third_layout.addWidget(clear_button)
        third_layout.addWidget(self.result_label)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(first_layout)
        main_layout.addLayout(second_layout)
        main_layout.addLayout(third_layout)

        # Add padding to main layout (left, top, right, bottom)
        main_layout.setContentsMargins(
            30, 30, 30, 10)

        # Central widget or container widget cz we cant pass a layout to setCentralWidget()
        container_widget = QWidget()
        container_widget.setLayout(main_layout)
        self.setCentralWidget(container_widget)

    def on_convert_button_clicked(self):
        try:
            # populate the respected properties
            self.feet_value = float(self.feet_input.text().strip())
            self.inches_value = float(self.inches_input.text().strip())
            if self.feet_value <= 0 or self.inches_value <= 0:
                # if any of input fields is a negative number, display a warning pop-up
                QMessageBox.warning(
                    self, "Warning", "Please enter positive values for feet and inches.")
            else:
                self.calculation = self.feet_value * 0.3048 + self.inches_value * 0.0254
                self.calculation = round(self.calculation, 2)
                # display the calculation result on result label
                self.result_label.setText(f"  {str(self.calculation)} meters")
        except ValueError:
            # if input fields are empty or not numbers, display a warning pop-up
            QMessageBox.warning(
                self, "Warning", "Please enter valid values for feet and inches.")

    def clear_fields(self):
        self.feet_input.clear()
        self.inches_input.clear()
        self.result_label.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # using sys.exit(app.exec()) instead of app.exec() below ensures the PyQt application closes cleanly
    # and exits the Python interpreter when the app finishes executing, allowing closure from the console.
    sys.exit(app.exec())
