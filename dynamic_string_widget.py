
import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QPushButton, QButtonGroup, QRadioButton,
                               QScrollArea, QFrame)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from typing import List, Tuple


class DynamicStringWidget(QWidget):
    """
    A dynamic widget that displays a list of strings with GUI/Custom radio buttons
    and returns the selected choices as a list of tuples.
    """
    # Signal emitted when OK is clicked, passes the result list
    result_ready = Signal(list)

    def __init__(self, string_list: List[str], parent=None):
        super().__init__(parent)
        self.string_list = string_list
        self.button_groups = []  # Store button groups for each string
        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface"""
        self.setWindowTitle("Dynamic String Widget")
        self.setMinimumSize(400, 300)

        # Main layout
        main_layout = QVBoxLayout()

        # Create scroll area for the string items
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameStyle(QFrame.NoFrame)

        # Content widget for scroll area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        # Create items for each string
        for i, string_item in enumerate(self.string_list, 1):
            item_frame = self.create_string_item(i, string_item)
            content_layout.addWidget(item_frame)

        content_layout.addStretch()  # Add stretch to push items to top
        scroll_area.setWidget(content_widget)

        # Add scroll area to main layout
        main_layout.addWidget(scroll_area)

        # Create OK button layout (right-aligned)
        button_layout = QHBoxLayout()
        button_layout.addStretch()  # Push button to the right

        self.ok_button = QPushButton("Okay")
        self.ok_button.setMinimumSize(80, 30)
        self.ok_button.clicked.connect(self.on_ok_clicked)
        button_layout.addWidget(self.ok_button)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def create_string_item(self, index: int, string_item: str) -> QFrame:
        """Create a frame containing the string label and radio buttons"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.StyledPanel)
        # frame.setStyleSheet("QFrame { margin: 5px; padding: 10px; }")

        layout = QVBoxLayout(frame)

        # String label with index
        label = QLabel(f"{index}. {string_item}")
        # font = QFont()
        # font.setPointSize(10)
        # font.setBold(True)
        # label.setFont(font)
        layout.addWidget(label)

        # Radio buttons layout
        radio_layout = QHBoxLayout()
        radio_layout.setContentsMargins(20, 5, 0, 5)  # Indent the radio buttons

        # Create button group for this string item
        button_group = QButtonGroup(self)

        # GUI radio button
        gui_radio = QRadioButton("GUI")
        # gui_radio.setChecked(True)  # Default selection
        button_group.addButton(gui_radio, 0)
        radio_layout.addWidget(gui_radio)

        # Custom radio button
        custom_radio = QRadioButton("Custom")
        button_group.addButton(custom_radio, 1)
        radio_layout.addWidget(custom_radio)

        radio_layout.addStretch()  # Push radio buttons to the left

        layout.addLayout(radio_layout)

        # Store the button group with the associated string
        self.button_groups.append((string_item, button_group))

        return frame

    def on_ok_clicked(self):
        """Handle OK button click and emit result"""
        result = self.get_result()
        self.result_ready.emit(result)
        self.close()

    def get_result(self) -> List[Tuple[str, str]]:
        """Get the current selection as a list of tuples"""
        result = []
        for string_item, button_group in self.button_groups:
            # Get the checked button ID (0 for GUI, 1 for Custom)
            checked_id = button_group.checkedId()
            choice = "GUI" if checked_id == 0 else "Custom"
            result.append((string_item, choice))
        return result


def main():
    """Example usage of the DynamicStringWidget"""
    app = QApplication(sys.argv)

    # Example input list
    input_list = ['string1', 'string2', 'string3']

    # Create and show the widget
    widget = DynamicStringWidget(input_list)

    # Connect the result signal to print the result
    def print_result(result):
        print("Selected choices:")
        for string_item, choice in result:
            print(f"  ('{string_item}', '{choice}')")
        print(f"\nResult list: {result}")

    widget.result_ready.connect(print_result)
    widget.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
