import sys
import random
from functools import partial
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QScrollArea, QLabel,
    QRadioButton, QHBoxLayout, QPushButton, QButtonGroup, QSizePolicy
)
from PySide6.QtCore import Qt

class ScrollableRadioWidget(QWidget):
    def __init__(self, max_visible_height=300, parent=None):
        super().__init__(parent)
        self.section_counter = 0
        self.button_groups = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(6)

        # Scroll area that will show scrollbars when content grows beyond max_visible_height
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Limit visible height so scrollbars appear when content grows
        self.scroll_area.setMaximumHeight(max_visible_height)

        # Content widget inside the scroll area
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.content_layout.setSpacing(8)
        self.content_layout.setContentsMargins(4, 4, 4, 4)

        # A stretch at the bottom so items stay at top when there's extra space
        self.content_layout.addStretch()

        self.scroll_area.setWidget(self.content_widget)
        layout.addWidget(self.scroll_area)

    def add_section(self, text, option1_text, option2_text):
        """Add a new section: bold label + two radio buttons (mutually exclusive)."""
        self.section_counter += 1

        # Remove the bottom stretch, add widgets, then add the stretch back
        # This keeps the stretch always at the end.
        # Pop the stretch item
        stretch_item = self.content_layout.takeAt(self.content_layout.count() - 1)

        # Label
        label = QLabel(f"Section {self.section_counter}: {text}")
        label.setWordWrap(True)
        label.setStyleSheet("font-weight: bold; margin: 6px 0 2px 0;")
        label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        self.content_layout.addWidget(label)

        # Radio buttons container (horizontal)
        radio_widget = QWidget()
        radio_layout = QHBoxLayout(radio_widget)
        radio_layout.setContentsMargins(12, 0, 0, 0)
        radio_layout.setSpacing(10)

        # ButtonGroup for mutual exclusivity
        button_group = QButtonGroup(self)
        self.button_groups.append(button_group)

        r1 = QRadioButton(option1_text)
        r2 = QRadioButton(option2_text)

        button_group.addButton(r1, 1)
        button_group.addButton(r2, 2)

        # Use partial to capture section index and option label
        r1.toggled.connect(partial(self._on_radio_toggled, self.section_counter, "A"))
        r2.toggled.connect(partial(self._on_radio_toggled, self.section_counter, "B"))

        radio_layout.addWidget(r1)
        radio_layout.addWidget(r2)
        radio_layout.addStretch()

        self.content_layout.addWidget(radio_widget)

        # Put the stretch back
        if stretch_item:
            self.content_layout.addItem(stretch_item)

        return button_group

    def _on_radio_toggled(self, section, option, checked):
        if checked:
            print(f"Section {section}: Option {option} selected")

    def get_selections(self):
        selections = {}
        for i, group in enumerate(self.button_groups, start=1):
            btn = group.checkedButton()
            if btn:
                selections[f"section_{i}"] = group.checkedId()
            else:
                selections[f"section_{i}"] = None
        return selections


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dynamic Scrollable Radio Sections")
        self.resize(520, 420)

        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)

        # Control buttons
        ctrl_layout = QHBoxLayout()
        add_btn = QPushButton("Add Section")
        get_btn = QPushButton("Get Selections")
        ctrl_layout.addWidget(add_btn)
        ctrl_layout.addWidget(get_btn)
        ctrl_layout.addStretch()
        main_layout.addLayout(ctrl_layout)

        # The reusable scrollable radio widget: set max visible height to 300 px
        self.radio_widget = ScrollableRadioWidget(max_visible_height=300)
        main_layout.addWidget(self.radio_widget)

        # Add initial sections
        self.radio_widget.add_section("Choose a color", "Red", "Blue")
        self.radio_widget.add_section("Favorite language?", "Python", "C++")
        self.radio_widget.add_section("Drink", "Coffee", "Tea")

        add_btn.clicked.connect(self.add_random_section)
        get_btn.clicked.connect(self.print_selections)

        self.setCentralWidget(container)

    def add_random_section(self):
        questions = [
            ("Cats or Dogs?", "Cats", "Dogs"),
            ("Morning or Night?", "Morning", "Night"),
            ("Tea or Coffee?", "Tea", "Coffee"),
            ("Remote or Office?", "Remote", "Office"),
        ]
        q = random.choice(questions)
        self.radio_widget.add_section(q[0], q[1], q[2])

    def print_selections(self):
        print(self.radio_widget.get_selections())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
