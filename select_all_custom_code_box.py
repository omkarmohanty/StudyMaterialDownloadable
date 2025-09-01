
import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QPushButton, QButtonGroup, QRadioButton,
                               QScrollArea, QFrame, QMessageBox, QGridLayout)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from typing import List, Tuple


class DynamicStringWidget(QWidget):
    """
    A dynamic widget that displays a list of strings with GUI/Custom radio buttons
    in a table-like layout and returns the selected choices as a list of tuples.
    Added select all/deselect all functionality via header buttons with smart column switching.
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
        self.setMinimumSize(450, 300)

        # Main layout
        main_layout = QVBoxLayout()

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

    def create_table_layout(self) -> QFrame:
        """Create a table-like layout with headers and radio buttons"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.StyledPanel)

        # Use QGridLayout for table-like appearance
        grid_layout = QGridLayout(frame)
        grid_layout.setSpacing(10)

        # Add headers
        # Empty cell for string column
        grid_layout.addWidget(QLabel(""), 0, 0)

        # GUI header button
        gui_button = QPushButton("GUI")
        gui_button.clicked.connect(self.select_all_gui)
        font = QFont()
        font.setBold(True)
        gui_button.setFont(font)
        grid_layout.addWidget(gui_button, 0, 1)

        # Custom header button
        custom_button = QPushButton("Custom")
        custom_button.clicked.connect(self.select_all_custom)
        custom_button.setFont(font)
        grid_layout.addWidget(custom_button, 0, 2)

        # Add rows for each string
        for i, string_item in enumerate(self.string_list, 1):
            row = i  # Start from row 1 (row 0 is headers)

            # String label
            string_label = QLabel(string_item)
            grid_layout.addWidget(string_label, row, 0)

            # Create button group for this string item
            button_group = QButtonGroup(self)

            # GUI radio button (centered)
            gui_radio = QRadioButton()
            gui_radio.setStyleSheet("QRadioButton { margin-left: 50%; margin-right: 50%; }")
            button_group.addButton(gui_radio, 0)
            grid_layout.addWidget(gui_radio, row, 1, Qt.AlignCenter)

            # Custom radio button (centered)
            custom_radio = QRadioButton()
            custom_radio.setStyleSheet("QRadioButton { margin-left: 50%; margin-right: 50%; }")
            button_group.addButton(custom_radio, 1)
            grid_layout.addWidget(custom_radio, row, 2, Qt.AlignCenter)

            # Store the button group with the associated string
            self.button_groups.append((string_item, button_group))

        return frame

    def are_all_gui_selected(self) -> bool:
        """Check if all GUI radio buttons are selected"""
        return all(bg.checkedId() == 0 for _, bg in self.button_groups)

    def are_all_custom_selected(self) -> bool:
        """Check if all Custom radio buttons are selected"""
        return all(bg.checkedId() == 1 for _, bg in self.button_groups)

    def select_all_gui(self):
        """Select all GUI radio buttons, or deselect all if all GUI are already selected"""
        if self.are_all_gui_selected():
            # All GUI are selected, so deselect all (clear all selections)
            self.clear_all_selections()
        else:
            # Select all GUI buttons (this will automatically deselect any Custom buttons due to radio button behavior)
            for _, button_group in self.button_groups:
                button_group.button(0).setChecked(True)

    def select_all_custom(self):
        """Select all Custom radio buttons, or deselect all if all Custom are already selected"""
        if self.are_all_custom_selected():
            # All Custom are selected, so deselect all (clear all selections)
            self.clear_all_selections()
        else:
            # Select all Custom buttons (this will automatically deselect any GUI buttons due to radio button behavior)
            for _, button_group in self.button_groups:
                button_group.button(1).setChecked(True)

    def clear_all_selections(self):
        """Clear all radio button selections"""
        for _, button_group in self.button_groups:
            # Get the currently checked button and uncheck it
            checked_button = button_group.checkedButton()
            if checked_button:
                checked_button.setAutoExclusive(False)  # Temporarily disable auto-exclusive
                checked_button.setChecked(False)        # Uncheck
                checked_button.setAutoExclusive(True)   # Re-enable auto-exclusive

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
    """Example usage of the DynamicStringWidget"""
    app = QApplication(sys.argv)

    # Example input list
    input_list = ['string1', 'string2', 'string3', 'string4', 'string5']

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

    print("Instructions:")
    print("â€¢ Click 'GUI' button to select all GUI options")
    print("â€¢ Click 'Custom' button to select all Custom options") 
    print("â€¢ If you click 'Custom' after 'GUI', it will switch all from GUI to Custom")
    print("â€¢ If you click the same button twice, it will deselect all")
    print("â€¢ Radio button behavior ensures only one option per row is selected")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
