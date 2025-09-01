
import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QPushButton, QButtonGroup, QRadioButton,
                               QScrollArea, QFrame, QMessageBox, QGridLayout, 
                               QCheckBox)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from typing import List, Tuple


class DynamicStringWidget(QWidget):
    """
    A dynamic widget that displays a list of strings with GUI/Custom radio buttons
    in a table-like layout with checkboxes for select all/deselect all functionality.
    """
    # Signal emitted when OK is clicked, passes the result list
    result_ready = Signal(list)

    def __init__(self, string_list: List[str], parent=None):
        super().__init__(parent)
        self.string_list = string_list
        self.button_groups = []  # Store button groups for each string
        self.gui_checkbox = None
        self.custom_checkbox = None
        self.updating_checkboxes = False  # Flag to prevent recursive updates
        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface"""
        self.setWindowTitle("Dynamic String Widget")
        self.setMinimumSize(500, 300)

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
        grid_layout.setSpacing(15)
        grid_layout.setContentsMargins(15, 15, 15, 15)

        # Add headers
        # Empty cell for string column
        grid_layout.addWidget(QLabel(""), 0, 0)

        # GUI column header
        gui_container = QWidget()
        gui_layout = QVBoxLayout(gui_container)
        gui_layout.setContentsMargins(0, 0, 0, 0)
        gui_layout.setSpacing(5)

        # GUI label
        gui_label = QLabel("GUI")
        gui_label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setBold(True)
        font.setPointSize(11)
        gui_label.setFont(font)
        gui_layout.addWidget(gui_label)

        # GUI checkbox (centered) - NO tristate, just binary
        gui_checkbox_container = QWidget()
        gui_checkbox_layout = QHBoxLayout(gui_checkbox_container)
        gui_checkbox_layout.setContentsMargins(0, 0, 0, 0)
        gui_checkbox_layout.addStretch()

        self.gui_checkbox = QCheckBox()
        self.gui_checkbox.setTristate(False)  # Only checked/unchecked states
        self.gui_checkbox.clicked.connect(self.on_gui_checkbox_clicked)  # Use clicked instead of stateChanged
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

        # Custom checkbox (centered) - NO tristate, just binary
        custom_checkbox_container = QWidget()
        custom_checkbox_layout = QHBoxLayout(custom_checkbox_container)
        custom_checkbox_layout.setContentsMargins(0, 0, 0, 0)
        custom_checkbox_layout.addStretch()

        self.custom_checkbox = QCheckBox()
        self.custom_checkbox.setTristate(False)  # Only checked/unchecked states
        self.custom_checkbox.clicked.connect(self.on_custom_checkbox_clicked)  # Use clicked instead of stateChanged
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
            gui_radio.toggled.connect(self.on_radio_button_changed)

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
            custom_radio.toggled.connect(self.on_radio_button_changed)

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

    def on_radio_button_changed(self):
        """Called when any radio button changes - update checkbox states accordingly"""
        if self.updating_checkboxes:
            return  # Avoid recursive updates

        self.update_checkbox_states_from_radios()

    def update_checkbox_states_from_radios(self):
        """Update checkbox states based on current radio button selections"""
        if self.updating_checkboxes:
            return

        self.updating_checkboxes = True

        gui_count = sum(1 for _, bg in self.button_groups if bg.checkedId() == 0)
        custom_count = sum(1 for _, bg in self.button_groups if bg.checkedId() == 1)
        total_count = len(self.button_groups)

        # Update GUI checkbox - only check if ALL are GUI selected
        self.gui_checkbox.setChecked(gui_count == total_count)

        # Update Custom checkbox - only check if ALL are Custom selected
        self.custom_checkbox.setChecked(custom_count == total_count)

        self.updating_checkboxes = False

    def on_gui_checkbox_clicked(self):
        """Handle GUI checkbox click"""
        if self.updating_checkboxes:
            return

        self.updating_checkboxes = True

        if self.gui_checkbox.isChecked():
            print("GUI checkbox checked - selecting all GUI radio buttons")
            # Select all GUI radio buttons
            for _, button_group in self.button_groups:
                button_group.button(0).setChecked(True)
            # Uncheck Custom checkbox
            self.custom_checkbox.setChecked(False)
        else:
            print("GUI checkbox unchecked - clearing all selections")
            # Clear all GUI selections
            self.clear_all_selections()

        self.updating_checkboxes = False

    def on_custom_checkbox_clicked(self):
        """Handle Custom checkbox click"""
        if self.updating_checkboxes:
            return

        self.updating_checkboxes = True

        if self.custom_checkbox.isChecked():
            print("Custom checkbox checked - selecting all Custom radio buttons")
            # Select all Custom radio buttons
            for _, button_group in self.button_groups:
                button_group.button(1).setChecked(True)
            # Uncheck GUI checkbox
            self.gui_checkbox.setChecked(False)
        else:
            print("Custom checkbox unchecked - clearing all selections")
            # Clear all Custom selections
            self.clear_all_selections()

        self.updating_checkboxes = False

    def clear_all_selections(self):
        """Clear all radio button selections"""
        for _, button_group in self.button_groups:
            checked_button = button_group.checkedButton()
            if checked_button:
                checked_button.setAutoExclusive(False)
                checked_button.setChecked(False)
                checked_button.setAutoExclusive(True)

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
    input_list = ['string1', 'string2', 'string3', 'string4']

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
    print("â€¢ Check the checkbox under GUI to select ALL GUI options")
    print("â€¢ Check the checkbox under Custom to select ALL Custom options") 
    print("â€¢ Checking one will automatically uncheck the other and switch all selections")
    print("â€¢ Unchecking will clear all selections")
    print("â€¢ Checkboxes only show checked âœ“ or unchecked â˜ (no partial state)")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()8
