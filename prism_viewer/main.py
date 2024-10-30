import sys
import sqlite3
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, \
    QWidget, QFrame
from prism_viewer.prism_calculator import PrismCalculator  # Import the PrismCalculator module
from prism_viewer.draw_rectangular_prism import create_rectangular_prism, display_prism  # Import the CAD functions


class PrismViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Rectangular Prism Viewer")
        self.setGeometry(100, 100, 1000, 600)

        # Create main widget and layout
        main_widget = QWidget()
        main_layout = QHBoxLayout()

        # Left side layout
        left_layout = QVBoxLayout()

        # Dropdown menu for designations
        self.designation_dropdown = QComboBox()
        self.designation_dropdown.currentIndexChanged.connect(self.update_display)
        left_layout.addWidget(self.designation_dropdown)

        # Labels to display surface area and volume
        self.surface_area_label = QLabel("Surface Area: ")
        left_layout.addWidget(self.surface_area_label)

        self.volume_label = QLabel("Volume: ")
        left_layout.addWidget(self.volume_label)

        # Button to display the 3D model
        self.display_button = QPushButton("Display 3D Model")
        self.display_button.clicked.connect(self.display_cad_model)
        left_layout.addWidget(self.display_button)

        # Add left layout to the main layout
        main_layout.addLayout(left_layout)

        # Right side layout (placeholder for additional content)
        right_frame = QFrame()
        right_frame.setFrameShape(QFrame.StyledPanel)
        right_layout = QVBoxLayout()

        # Example content for the right side window
        right_label = QLabel("Additional Content")
        right_layout.addWidget(right_label)

        right_frame.setLayout(right_layout)

        # Add right layout to the main layout
        main_layout.addWidget(right_frame)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Database connection
        self.conn = sqlite3.connect('prisms.db')
        self.cursor = self.conn.cursor()

        # Load data into NumPy array
        self.cursor.execute('SELECT * FROM prisms')
        rows = self.cursor.fetchall()
        dtype = [('designation', 'U10'), ('length', 'f8'), ('width', 'f8'), ('height', 'f8')]
        self.data = np.array(rows, dtype=dtype)

        # Populate dropdown
        self.designation_dropdown.addItems(self.data['designation'].tolist())

    def update_display(self):
        selected_designation = self.designation_dropdown.currentText()
        prism_data = self.data[self.data['designation'] == selected_designation][0]
        length, width, height = prism_data['length'], prism_data['width'], prism_data['height']

        surface_area = PrismCalculator.surface_area(length, width, height)
        volume = PrismCalculator.volume(length, width, height)

        # Update labels
        self.surface_area_label.setText(f"Surface Area: {surface_area}")
        self.volume_label.setText(f"Volume: {volume}")

    def display_cad_model(self):
        selected_designation = self.designation_dropdown.currentText()
        prism_data = self.data[self.data['designation'] == selected_designation][0]
        length, width, height = prism_data['length'], prism_data['width'], prism_data['height']

        box = create_rectangular_prism(length, width, height)
        display_prism(box)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = PrismViewer()
    viewer.show()
    sys.exit(app.exec_())
