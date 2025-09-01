
import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QPushButton, QButtonGroup, QRadioButton,
                               QScrollArea, QFrame, QMessageBox, QGridLayout)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from typing import List, Tuple


class EnhancedTableDynamicWidget(QWidget):
    """
    Enhanced dynamic widget with table-like layout and better styling.
    """
    result_ready = Signal(list)

    def __init__(self, string_list: List[str], parent=None):
        super().__init__(parent)
        self.string_list = string_list
        self.button_groups = []
        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface with enhanced styling"""
        self.setWindowTitle("Dynamic String Widget")
        self.setMinimumSize(500, 350)

        # Apply styling
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QFrame {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 15px;
            }
            QLabel {
                color: #495057;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
        """)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Title
        title_label = QLabel("Select configuration for each item:")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #212529; margin-bottom: 10px;")
        main_layout.addWidget(title_label)

        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameStyle(QFrame.NoFrame)
        scroll_area.setStyleSheet("QScrollArea { background-color: transparent; }")

        # Content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        # Create the table
        table_frame = self.create_enhanced_table()
        content_layout.addWidget(table_frame)
        content_layout.addStretch()

        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.ok_button = QPushButton("Okay")
        self.ok_button.setMinimumSize(100, 40)
        self.ok_button.clicked.connect(self.on_ok_clicked)
        button_layout.addWidget(self.ok_button)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def create_enhanced_table(self) -> QFrame:
        """Create an enhanced table layout"""
        frame = QFrame()

        # Grid layout
        grid_layout = QGridLayout(frame)
        grid_layout.setSpacing(15)
        grid_layout.setContentsMargins(20, 20, 20, 20)

        # Set column stretch to make columns evenly distributed
        grid_layout.setColumnStretch(0, 2)  # String column wider
        grid_layout.setColumnStretch(1, 1)  # GUI column
        grid_layout.setColumnStretch(2, 1)  # Custom column

        # Headers with styling
        empty_header = QLabel("")
        grid_layout.addWidget(empty_header, 0, 0)

        gui_header = QLabel("GUI")
        gui_header.setAlignment(Qt.AlignCenter)
        gui_header.setStyleSheet("""
            QLabel {
                font-size: 12pt;
                font-weight: bold;
                color: #007bff;
                padding: 8px;
                border-bottom: 2px solid #007bff;
            }
        """)
        grid_layout.addWidget(gui_header, 0, 1)

        custom_header = QLabel("Custom")
        custom_header.setAlignment(Qt.AlignCenter)
        custom_header.setStyleSheet("""
            QLabel {
                font-size: 12pt;
                font-weight: bold;
                color: #28a745;
                padding: 8px;
                border-bottom: 2px solid #28a745;
            }
        """)
        grid_layout.addWidget(custom_header, 0, 2)

        # Add rows for each string
        for i, string_item in enumerate(self.string_list):
            row = i + 1

            # String label with styling
            string_label = QLabel(string_item)
            string_label.setStyleSheet("""
                QLabel {
                    font-size: 11pt;
                    font-weight: 500;
                    color: #343a40;
                    padding: 8px;
                    background-color: #f8f9fa;
                    border-radius: 4px;
                }
            """)
            grid_layout.addWidget(string_label, row, 0)

            # Button group
            button_group = QButtonGroup(self)

            # GUI radio button
            gui_radio = QRadioButton()
            gui_radio.setStyleSheet("""
                QRadioButton::indicator {
                    width: 18px;
                    height: 18px;
                    border-radius: 9px;
                    border: 2px solid #007bff;
                    background-color: white;
                }
                QRadioButton::indicator:checked {
                    background-color: #007bff;
                    border: 2px solid #007bff;
                }
                QRadioButton::indicator:hover {
                    border: 2px solid #0056b3;
                }
            """)
            button_group.addButton(gui_radio, 0)

            # Create container for centering
            gui_container = QWidget()
            gui_layout = QHBoxLayout(gui_container)
            gui_layout.addStretch()
            gui_layout.addWidget(gui_radio)
            gui_layout.addStretch()
            gui_layout.setContentsMargins(0, 0, 0, 0)
            grid_layout.addWidget(gui_container, row, 1)

            # Custom radio button
            custom_radio = QRadioButton()
            custom_radio.setStyleSheet("""
                QRadioButton::indicator {
                    width: 18px;
                    height: 18px;
                    border-radius: 9px;
                    border: 2px solid #28a745;
                    background-color: white;
                }
                QRadioButton::indicator:checked {
                    background-color: #28a745;
                    border: 2px solid #28a745;
                }
                QRadioButton::indicator:hover {
                    border: 2px solid #1e7e34;
                }
            """)
            button_group.addButton(custom_radio, 1)

            # Create container for centering
            custom_container = QWidget()
            custom_layout = QHBoxLayout(custom_container)
            custom_layout.addStretch()
            custom_layout.addWidget(custom_radio)
            custom_layout.addStretch()
            custom_layout.setContentsMargins(0, 0, 0, 0)
            grid_layout.addWidget(custom_container, row, 2)

            self.button_groups.append((string_item, button_group))

        return frame

    def on_ok_clicked(self):
        """Handle OK button click with validation"""
        unselected_items = []
        for string_item, button_group in self.button_groups:
            if button_group.checkedId() == -1:
                unselected_items.append(string_item)

        if unselected_items:
            items_text = ", ".join(unselected_items)
            QMessageBox.warning(
                self, 
                "Incomplete Selection", 
                f"Please select options for: {items_text}",
                QMessageBox.Ok
            )
            return

        result = self.get_result()
        self.result_ready.emit(result)
        self.close()

    def get_result(self) -> List[Tuple[str, str]]:
        """Get the current selection as a list of tuples"""
        result = []
        for string_item, button_group in self.button_groups:
            checked_id = button_group.checkedId()
            choice = "GUI" if checked_id == 0 else "Custom"
            result.append((string_item, choice))
        return result


def main():
    """Example usage"""
    app = QApplication(sys.argv)

    # Example input list
    input_list = ['string1', 'string2', 'string3', 'string4', 'string5']

    widget = EnhancedTableDynamicWidget(input_list)

    def print_result(result):
        print("\nSelected choices:")
        for string_item, choice in result:
            print(f"  ('{string_item}', '{choice}')")
        print(f"\nResult list: {result}")

    widget.result_ready.connect(print_result)
    widget.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
