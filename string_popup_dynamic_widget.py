
import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QPushButton, QButtonGroup, QRadioButton,
                               QScrollArea, QFrame, QMessageBox, QGridLayout, 
                               QCheckBox, QTextEdit)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from typing import List, Tuple, Optional


class DynamicStringWidget(QWidget):
    """
    A dynamic widget that displays a list of strings with GUI/Custom radio buttons
    in a table-like layout with checkboxes for select all/deselect all functionality.
    Now includes an optional text box at the top.
    """
    # Signal emitted when OK is clicked, passes the result list
    result_ready = Signal(list)

    def __init__(self, string_list: List[str], box_text: Optional[str] = None, parent=None):
        super().__init__(parent)
        self.string_list = string_list
        self.box_text = box_text
        self.button_groups = []  # Store button groups for each string
        self.gui_checkbox = None
        self.custom_checkbox = None
        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface"""
        self.setWindowTitle("Dynamic String Widget")
        self.setMinimumSize(500, 300)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Add text box at the top if text is provided
        if self.box_text:
            text_box = self.create_text_box()
            main_layout.addWidget(text_box)

        # Create scroll area for the string items
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameStyle(QFrame.NoFrame)

        # Content widget for scroll area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        # Create the table-like layout
        table_frame = self.create_table_layout()
        content_layout.addWidget(table_frame)

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

    def create_text_box(self) -> QFrame:
        """Create a text box frame to display the provided text"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                padding: 10px;
                margin-bottom: 10px;
            }
        """)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(15, 15, 15, 15)

        # Create text display
        text_label = QLabel(self.box_text)
        text_label.setWordWrap(True)  # Allow text wrapping
        text_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        text_label.setStyleSheet("""
            QLabel {
                background-color: transparent;
                border: none;
                font-size: 11pt;
                color: #495057;
                line-height: 1.4;
            }
        """)

        layout.addWidget(text_label)

        return frame

    def create_table_layout(self) -> QFrame:
        """Create a table-like layout with headers and radio buttons"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.StyledPanel)

        # Use QGridLayout for table-like appearance
        grid_layout = QGridLayout(frame)
        grid_layout.setSpacing(15)
        grid_layout.setContentsMargins(15, 15, 15, 15)

        # Add headers
        # STRING COLUMN HEADER
        string_header = QLabel("Duplicate API Name")
        string_header.setAlignment(Qt.AlignLeft)
        font = QFont()
        font.setBold(True)
        font.setPointSize(11)
        string_header.setFont(font)
        grid_layout.addWidget(string_header, 0, 0)

        # GUI column header
        gui_container = QWidget()
        gui_layout = QVBoxLayout(gui_container)
        gui_layout.setContentsMargins(0, 0, 0, 0)
        gui_layout.setSpacing(5)

        # GUI label
        gui_label = QLabel("GUI")
        gui_label.setAlignment(Qt.AlignCenter)
        gui_label.setFont(font)
        gui_layout.addWidget(gui_label)

        # GUI checkbox (centered)
        gui_checkbox_container = QWidget()
        gui_checkbox_layout = QHBoxLayout(gui_checkbox_container)
        gui_checkbox_layout.setContentsMargins(0, 0, 0, 0)
        gui_checkbox_layout.addStretch()

        self.gui_checkbox = QCheckBox()
        self.gui_checkbox.setTristate(False)
        self.gui_checkbox.clicked.connect(self.on_gui_checkbox_clicked)
        gui_checkbox_layout.addWidget(self.gui_checkbox)
        gui_checkbox_layout.addStretch()

        gui_layout.addWidget(gui_checkbox_container)
        grid_layout.addWidget(gui_container, 0, 1)

        # Custom column header
        custom_container = QWidget()
        custom_layout = QVBoxLayout(custom_container)
        custom_layout.setContentsMargins(0, 0, 0, 0)
        custom_layout.setSpacing(5)

        # Custom label
        custom_label = QLabel("Custom")
        custom_label.setAlignment(Qt.AlignCenter)
        custom_label.setFont(font)
        custom_layout.addWidget(custom_label)

        # Custom checkbox (centered)
        custom_checkbox_container = QWidget()
        custom_checkbox_layout = QHBoxLayout(custom_checkbox_container)
        custom_checkbox_layout.setContentsMargins(0, 0, 0, 0)
        custom_checkbox_layout.addStretch()

        self.custom_checkbox = QCheckBox()
        self.custom_checkbox.setTristate(False)
        self.custom_checkbox.clicked.connect(self.on_custom_checkbox_clicked)
        custom_checkbox_layout.addWidget(self.custom_checkbox)
        custom_checkbox_layout.addStretch()

        custom_layout.addWidget(custom_checkbox_container)
        grid_layout.addWidget(custom_container, 0, 2)

        # Add rows for each string
        for i, string_item in enumerate(self.string_list, 1):
            row = i  # Start from row 1 (row 0 is headers)

            # String label
            string_label = QLabel(string_item)
            string_label.setStyleSheet("QLabel { font-size: 10pt; }")
            grid_layout.addWidget(string_label, row, 0)

            # Create button group for this string item
            button_group = QButtonGroup(self)

            # GUI radio button (centered)
            gui_radio = QRadioButton()
            button_group.addButton(gui_radio, 0)

            # Center the radio button
            gui_radio_container = QWidget()
            gui_radio_layout = QHBoxLayout(gui_radio_container)
            gui_radio_layout.setContentsMargins(0, 0, 0, 0)
            gui_radio_layout.addStretch()
            gui_radio_layout.addWidget(gui_radio)
            gui_radio_layout.addStretch()
            grid_layout.addWidget(gui_radio_container, row, 1)

            # Custom radio button (centered)
            custom_radio = QRadioButton()
            button_group.addButton(custom_radio, 1)

            # Center the radio button
            custom_radio_container = QWidget()
            custom_radio_layout = QHBoxLayout(custom_radio_container)
            custom_radio_layout.setContentsMargins(0, 0, 0, 0)
            custom_radio_layout.addStretch()
            custom_radio_layout.addWidget(custom_radio)
            custom_radio_layout.addStretch()
            grid_layout.addWidget(custom_radio_container, row, 2)

            # Store the button group with the associated string
            self.button_groups.append((string_item, button_group))

        return frame

    def on_gui_checkbox_clicked(self):
        """Handle GUI checkbox click - auto-switch behavior"""
        if self.gui_checkbox.isChecked():
            # Select all GUI radios
            for _, bg in self.button_groups:
                bg.button(0).setChecked(True)
            # Uncheck Custom
            self.custom_checkbox.setChecked(False)
        else:
            # GUI was unchecked â†’ auto-select all Custom
            for _, bg in self.button_groups:
                bg.button(1).setChecked(True)
            # Check Custom checkbox
            self.custom_checkbox.setChecked(True)

    def on_custom_checkbox_clicked(self):
        """Handle Custom checkbox click - auto-switch behavior"""
        if self.custom_checkbox.isChecked():
            # Select all Custom radios
            for _, bg in self.button_groups:
                bg.button(1).setChecked(True)
            # Uncheck GUI
            self.gui_checkbox.setChecked(False)
        else:
            # Custom was unchecked â†’ auto-select all GUI
            for _, bg in self.button_groups:
                bg.button(0).setChecked(True)
            self.gui_checkbox.setChecked(True)

    def on_ok_clicked(self):
        """Handle OK button click with validation"""
        # Check if all selections are made
        unselected_items = []
        for string_item, button_group in self.button_groups:
            if button_group.checkedId() == -1:  # -1 means no selection
                unselected_items.append(string_item)

        # If there are unselected items, show warning and return
        if unselected_items:
            QMessageBox.warning(
                self, 
                "Incomplete Selection", 
                "Please select all options before proceeding.",
                QMessageBox.Ok
            )
            return

        # If all selections are made, proceed
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
    """Example usage of the DynamicStringWidget with and without text box"""
    app = QApplication(sys.argv)

    # Example 1: With text box
    print("Example 1: Widget with text box")
    input_list1 = ['getUserData', 'fetchUserInfo', 'getProfile']
    box_text1 = """The following API names appear to be duplicates based on similar functionality. 
Please select whether each should be handled by GUI components or Custom logic.

Note: GUI handling will use standard interface patterns, while Custom will require specialized implementation."""

    widget1 = DynamicStringWidget(input_list1, box_text1)

    def print_result1(result):
        print("Result with text box:")
        for string_item, choice in result:
            print(f"  ('{string_item}', '{choice}')")
        print(f"\nResult list: {result}")

        # Show example 2 after first one closes
        show_example2()

    widget1.result_ready.connect(print_result1)
    widget1.show()

    def show_example2():
        # Example 2: Without text box
        print("\nExample 2: Widget without text box")
        input_list2 = ['loadUserData', 'retrieveUser']

        widget2 = DynamicStringWidget(input_list2)  # No box_text parameter

        def print_result2(result):
            print("Result without text box:")
            for string_item, choice in result:
                print(f"  ('{string_item}', '{choice}')")
            print(f"\nResult list: {result}")

        widget2.result_ready.connect(print_result2)
        widget2.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
