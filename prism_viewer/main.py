import sys
import sqlite3
import numpy as np
from typing import Tuple, Optional
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, 
    QComboBox, QPushButton, QWidget, QFrame, QMessageBox
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Display.SimpleGui import init_display
from prism_viewer.prism_calculator import PrismCalculator
from prism_viewer.draw_rectangular_prism import create_rectangular_prism

class DisplayThread(QThread):
    """Thread for handling 3D model creation without blocking the GUI."""
    
    finished = pyqtSignal(object)  # Signal to emit the created box
    error = pyqtSignal(str)        # Signal for error handling
    
    def __init__(self, length: float, width: float, height: float):
        super().__init__()
        self.length = length
        self.width = width
        self.height = height
        
    def run(self):
        try:
            box = create_rectangular_prism(
                length=self.length,
                width=self.width,  
                height=self.height
            )
            self.finished.emit(box)
        except Exception as e:
            self.error.emit(str(e))


import sys
import sqlite3
import numpy as np
from typing import Tuple, Optional
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, 
    QComboBox, QPushButton, QWidget, QFrame, QMessageBox
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QFont, QPalette, QColor
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Display.SimpleGui import init_display
from prism_viewer.prism_calculator import PrismCalculator
from prism_viewer.draw_rectangular_prism import create_rectangular_prism

class DisplayThread(QThread):
    finished = pyqtSignal(object)
    error = pyqtSignal(str)
    
    def __init__(self, length: float, width: float, height: float):
        super().__init__()
        self.length = length
        self.width = width
        self.height = height
        
    def run(self):
        try:
            box = create_rectangular_prism(
                length=self.length,
                width=self.width,  
                height=self.height
            )
            self.finished.emit(box)
        except Exception as e:
            self.error.emit(str(e))

class PrismViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.display_thread = None
        self.data = None
        self.conn = None
        self.cursor = None
        self.display = None
        self.start_display = None
        self.initUI()
        self.setupDatabase()
        self.initializeOCC()
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f7fa;
            }
            QLabel {
                color: #2c3e50;
                font-size: 12px;
            }
            QComboBox {
                background-color: white;
                border: 1px solid #dce4ec;
                border-radius: 4px;
                padding: 6px;
                min-width: 200px;
                color: #2c3e50;
            }
            QComboBox:drop-down {
                border: none;
                padding-right: 20px;
            }
            QComboBox:down-arrow {
                width: 12px;
                height: 12px;
            }
            QFrame {
                background-color: white;
                border: 1px solid #dce4ec;
                border-radius: 6px;
                padding: 10px;
            }
        """)
        
    def initializeOCC(self):
        self.display, self.start_display, add_menu, add_function_to_menu = init_display()
        
    def initUI(self):
        self.setWindowTitle("Advanced Rectangular Prism Viewer")
        self.setGeometry(100, 100, 1200, 800)

        main_widget = QWidget()
        main_widget.setStyleSheet("background-color: #f5f7fa;")
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        left_panel = self.createLeftPanel()
        main_layout.addLayout(left_panel, stretch=1)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def createLeftPanel(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Title with enhanced styling
        title_label = QLabel("Prism Controls")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #34495e;
            padding: 10px 0;
        """)
        layout.addWidget(title_label)

        # Dropdown section
        dropdown_label = QLabel("Select Prism:")
        dropdown_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(dropdown_label)
        
        self.designation_dropdown = QComboBox()
        self.designation_dropdown.currentIndexChanged.connect(self.update_display)
        layout.addWidget(self.designation_dropdown)

        # Information display with enhanced styling
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #dce4ec;
                border-radius: 8px;
                padding: 15px;
            }
            QLabel {
                font-size: 13px;
                color: #2c3e50;
                padding: 5px 0;
            }
        """)
        
        info_layout = QVBoxLayout()
        
        info_title = QLabel("Prism Information")
        info_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #34495e;")
        info_layout.addWidget(info_title)
        
        self.dimension_label = QLabel("Dimensions: ")
        self.surface_area_label = QLabel("Surface Area: ")
        self.volume_label = QLabel("Volume: ")
        
        for label in [self.dimension_label, self.surface_area_label, self.volume_label]:
            info_layout.addWidget(label)
        
        info_frame.setLayout(info_layout)
        layout.addWidget(info_frame)

        # Status label
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("""
            color: #3498db;
            font-size: 13px;
            padding: 10px 0;
        """)
        layout.addWidget(self.status_label)

        # Buttons with modern styling
        self.display_button = QPushButton("Display 3D Model")
        self.display_button.clicked.connect(self.start_display_thread)
        self.display_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        layout.addWidget(self.display_button)

        self.clear_button = QPushButton("Clear View")
        self.clear_button.clicked.connect(self.clear_display)
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        layout.addWidget(self.clear_button)

        layout.addStretch()
        return layout

    # [Rest of the methods remain unchanged]

    def setupDatabase(self):
        try:
            self.conn = sqlite3.connect('prisms.db')
            self.cursor = self.conn.cursor()
            
            self.cursor.execute('SELECT * FROM prisms')
            rows = self.cursor.fetchall()
            dtype = [('designation', 'U10'), ('length', 'f8'), ('width', 'f8'), ('height', 'f8')]
            self.data = np.array(rows, dtype=dtype)
            
            self.designation_dropdown.addItems(self.data['designation'].tolist())
            
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error",
                               f"Failed to connect to database: {str(e)}")
            self.close()
    
    def update_display(self):
        try:
            selected_designation = self.designation_dropdown.currentText()
            prism_data = self.data[self.data['designation'] == selected_designation][0]
            length, width, height = prism_data['length'], prism_data['width'], prism_data['height']

            self.dimension_label.setText(
                f"Dimensions: {length:.2f} x {width:.2f} x {height:.2f} units"
            )

            surface_area = PrismCalculator.surface_area(length, width, height)
            volume = PrismCalculator.volume(length, width, height)

            self.surface_area_label.setText(f"Surface Area: {surface_area:.2f} units²")
            self.volume_label.setText(f"Volume: {volume:.2f} units³")
            
        except Exception as e:
            self.status_label.setText(f"Error updating display: {str(e)}")
            self.status_label.setStyleSheet("color: red;")

    def start_display_thread(self):
        self.display_button.setEnabled(False)
        self.status_label.setText("Preparing 3D model...")
        self.status_label.setStyleSheet("color: blue;")
        
        try:
            selected_designation = self.designation_dropdown.currentText()
            prism_data = self.data[self.data['designation'] == selected_designation][0]
            length, width, height = prism_data['length'], prism_data['width'], prism_data['height']

            self.display_thread = DisplayThread(length, width, height)
            self.display_thread.finished.connect(self.display_3d_model)
            self.display_thread.error.connect(self.handle_display_error)
            self.display_thread.start()
            
        except Exception as e:
            self.handle_display_error(str(e))

    def display_3d_model(self, box):
        try:
            self.status_label.setText("Displaying 3D model...")
            self.display.EraseAll()  # Clear previous display
            self.display.DisplayShape(box, update=True)
            self.display.View_Iso()
            self.display.FitAll()
            self.status_label.setText("3D model displayed successfully!")
            self.status_label.setStyleSheet("color: green;")
        except Exception as e:
            self.handle_display_error(str(e))
        finally:
            self.display_button.setEnabled(True)
            self.display_thread = None

    def clear_display(self):
        """Clear the 3D display"""
        try:
            if self.display:
                self.display.EraseAll()
                self.display.Repaint()
                self.status_label.setText("View cleared")
                self.status_label.setStyleSheet("color: blue;")
        except Exception as e:
            self.handle_display_error(str(e))

    def handle_display_error(self, error_msg: str):
        self.status_label.setText(f"Error: {error_msg}")
        self.status_label.setStyleSheet("color: red;")
        self.display_button.setEnabled(True)
        self.display_thread = None
        
        QMessageBox.warning(self, "Display Error", 
                          f"Failed to display 3D model: {error_msg}")

    def closeEvent(self, event):
        if self.conn:
            self.conn.close()
        event.accept()


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        viewer = PrismViewer()
        viewer.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)