import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QScrollArea, QLabel, QRadioButton, QHBoxLayout, 
                               QPushButton, QButtonGroup, QSizePolicy)
from PySide6.QtCore import Qt

class DynamicRadioWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dynamic Widget with Text and Radio Buttons")
        self.setGeometry(300, 300, 400, 600)
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        
        # Add button to dynamically add content
        add_button = QPushButton("Add Text and Radio Buttons")
        add_button.clicked.connect(self.add_content_section)
        main_layout.addWidget(add_button)
        
        # Create scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Create scrollable widget and layout
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Set the scrollable widget to the scroll area
        self.scroll_area.setWidget(self.scroll_widget)
        main_layout.addWidget(self.scroll_area)
        
        # Counter for unique naming
        self.section_counter = 0
        self.button_groups = []
        
        # Add some initial content
        for i in range(3):
            self.add_content_section()
    
    def add_content_section(self):
        """Add a section with text and two radio buttons"""
        self.section_counter += 1
        
        # Create text label
        text_label = QLabel(f"Section {self.section_counter}: Choose an option")
        text_label.setStyleSheet("font-weight: bold; margin-top: 10px; margin-bottom: 5px;")
        self.scroll_layout.addWidget(text_label)
        
        # Create container for radio buttons
        radio_container = QWidget()
        radio_layout = QHBoxLayout(radio_container)
        radio_layout.setContentsMargins(20, 0, 0, 0)  # Indent radio buttons
        
        # Create button group for mutual exclusivity
        button_group = QButtonGroup(self)
        self.button_groups.append(button_group)
        
        # Create two radio buttons
        radio1 = QRadioButton(f"Option A-{self.section_counter}")
        radio2 = QRadioButton(f"Option B-{self.section_counter}")
        
        # Add radio buttons to the button group
        button_group.addButton(radio1, 1)
        button_group.addButton(radio2, 2)
        
        # Connect signals to handle selection
        radio1.toggled.connect(lambda checked, section=self.section_counter, option="A": 
                              self.on_radio_toggled(checked, section, option))
        radio2.toggled.connect(lambda checked, section=self.section_counter, option="B": 
                              self.on_radio_toggled(checked, section, option))
        
        # Add radio buttons to layout
        radio_layout.addWidget(radio1)
        radio_layout.addWidget(radio2)
        radio_layout.addStretch()  # Push buttons to the left
        
        # Add radio container to scroll layout
        self.scroll_layout.addWidget(radio_container)
        
        # Update scroll area to accommodate new content
        self.scroll_widget.adjustSize()
    
    def on_radio_toggled(self, checked, section, option):
        """Handle radio button selection"""
        if checked:
            print(f"Section {section}: Option {option} selected")

class ScrollableRadioWidget(QWidget):
    """Alternative implementation as a reusable widget"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.section_counter = 0
        self.button_groups = []
    
    def setup_ui(self):
        """Setup the UI components"""
        layout = QVBoxLayout(self)
        
        # Create scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Create scrollable content widget
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Set size policy to ensure proper resizing
        self.content_widget.setSizePolicy(QSizePolicy.Policy.Preferred, 
                                         QSizePolicy.Policy.MinimumExpanding)
        
        # Connect the content widget to scroll area
        self.scroll_area.setWidget(self.content_widget)
        layout.addWidget(self.scroll_area)
    
    def add_section(self, text, option1_text, option2_text):
        """Add a new section with custom text and radio button labels"""
        self.section_counter += 1
        
        # Text label
        label = QLabel(text)
        label.setStyleSheet("font-weight: bold; margin: 10px 0 5px 0;")
        label.setWordWrap(True)
        self.content_layout.addWidget(label)
        
        # Radio buttons container
        radio_widget = QWidget()
        radio_layout = QVBoxLayout(radio_widget)
        radio_layout.setContentsMargins(15, 0, 0, 5)
        
        # Button group for mutual exclusivity
        button_group = QButtonGroup(self)
        self.button_groups.append(button_group)
        
        # Radio buttons
        radio1 = QRadioButton(option1_text)
        radio2 = QRadioButton(option2_text)
        
        button_group.addButton(radio1, 1)
        button_group.addButton(radio2, 2)
        
        radio_layout.addWidget(radio1)
        radio_layout.addWidget(radio2)
        
        self.content_layout.addWidget(radio_widget)
        
        # Update scroll area
        self.content_widget.adjustSize()
        
        return button_group
    
    def get_selections(self):
        """Get all current selections"""
        selections = {}
        for i, group in enumerate(self.button_groups):
            if group.checkedButton():
                selections[f"section_{i+1}"] = group.checkedId()
        return selections

# Example usage with the reusable widget
class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reusable Dynamic Radio Widget")
        self.setGeometry(300, 300, 500, 400)
        
        # Create main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Add control buttons
        button_layout = QHBoxLayout()
        add_button = QPushButton("Add Section")
        get_selections_button = QPushButton("Get Selections")
        
        add_button.clicked.connect(self.add_new_section)
        get_selections_button.clicked.connect(self.show_selections)
        
        button_layout.addWidget(add_button)
        button_layout.addWidget(get_selections_button)
        layout.addLayout(button_layout)
        
        # Create the scrollable radio widget
        self.radio_widget = ScrollableRadioWidget()
        layout.addWidget(self.radio_widget)
        
        # Add some initial sections
        self.radio_widget.add_section("What is your favorite color?", "Red", "Blue")
        self.radio_widget.add_section("What is your preferred programming language?", "Python", "JavaScript")
        self.radio_widget.add_section("Do you prefer coffee or tea?", "Coffee", "Tea")
    
    def add_new_section(self):
        """Add a new section dynamically"""
        import random
        questions = [
            ("What's your favorite season?", "Summer", "Winter"),
            ("Do you prefer cats or dogs?", "Cats", "Dogs"),
            ("What's your preferred work style?", "Remote", "Office"),
            ("What's your favorite meal?", "Breakfast", "Dinner"),
        ]
        question = random.choice(questions)
        self.radio_widget.add_section(question[0], question[1], question[2])
    
    def show_selections(self):
        """Display current selections"""
        selections = self.radio_widget.get_selections()
        print("Current selections:", selections)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # You can use either implementation:
    # window = DynamicRadioWidget()  # First implementation
    window = MainApp()  # Second implementation with reusable widget
    
    window.show()
    sys.exit(app.exec())
