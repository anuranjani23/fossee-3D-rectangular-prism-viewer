import unittest
import sqlite3
import sys
from PyQt5.QtWidgets import QApplication
from prism_viewer.main import PrismViewer
from prism_viewer.prism_calculator import PrismCalculator

class TestPrismViewerApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize the test database.
        cls.conn = sqlite3.connect('prisms.db')
        cls.cursor = cls.conn.cursor()
        
        # Create the application instance.
        cls.app = QApplication(sys.argv)
        cls.viewer = PrismViewer()
    
    def setUp(self):
        # Reset the application state before each test.
        self.viewer.designation_dropdown.setCurrentIndex(0)

    def test_program_initialization(self):
        self.assertEqual(self.viewer.windowTitle(), "Rectangular Prism Viewer")
        
        # Verify essential UI components.
        self.assertIsNotNone(self.viewer.designation_dropdown)
        self.assertIsNotNone(self.viewer.surface_area_label)
        self.assertIsNotNone(self.viewer.volume_label)
        self.assertIsNotNone(self.viewer.display_button)
        
        # Check the database connections.
        self.assertIsNotNone(self.viewer.conn)
        self.assertIsNotNone(self.viewer.cursor)
        
        # Check if the viewer has been created or not.
        self.assertTrue(self.viewer.isHidden())  

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()



class TestPrismCalculator(unittest.TestCase):

    def test_surface_area_calculation(self):
        test_cases = [
            # (length, width, height, expected_area = 2 * (length * width + width * height + height * length))
            (10, 5, 2, 2 * (10 * 5 + 5 * 2 + 2 * 10)),   # Standard case
            (1, 1, 1, 6),                                # Unit cube
            (10, 10, 10, 600),                           # Equal dimensions
        ]
        
        for length, width, height, expected in test_cases:
            with self.subTest(f"Testing surface area with L={length}, W={width}, H={height}"):
                result = PrismCalculator.surface_area(length, width, height)
                self.assertEqual(result, expected)

    def test_volume_calculation(self):
        test_cases = [
            # (length, width, height, expected_volume = length * width * height)
            (10, 5, 2, 10*5*2),  # Standard case
            (1, 1, 1, 1),        # Unit cube
            (10, 10, 10, 1000),  # Equal dimensions
        ]
        
        for length, width, height, expected in test_cases:
            with self.subTest(f"Testing volume with L={length}, W={width}, H={height}"):
                result = PrismCalculator.volume(length, width, height)
                self.assertEqual(result, expected)
    
    def test_zero_value_calculation(self):
        # Test case: To check if zero is returned for zero dimensions.
        # Surface area tests
        self.assertEqual(PrismCalculator.surface_area(0, 0, 0), 0)
        self.assertEqual(PrismCalculator.surface_area(5, 0, 0), 0)
        self.assertEqual(PrismCalculator.surface_area(0, 5, 0), 0)
        self.assertEqual(PrismCalculator.surface_area(0, 0, 5), 0)
        
        # Volume tests
        self.assertEqual(PrismCalculator.volume(0, 0, 0), 0)
        self.assertEqual(PrismCalculator.volume(0, 5, 2), 0)
        self.assertEqual(PrismCalculator.volume(5, 0, 2), 0)
        self.assertEqual(PrismCalculator.volume(5, 2, 0), 0)

    def test_negative_value_calculation(self):
        # Test case: To ensure handling of errors for negative values.
        negative_cases = [
            (-10, 5, 2),
            (10, -5, 2),
            (10, 5, -2),
            (-1, -1, -1)
        ]
    
        for length, width, height in negative_cases:
            with self.subTest(f"Testing negative values L={length}, W={width}, H={height}"):
                with self.assertRaises(ValueError):
                    PrismCalculator.surface_area(length, width, height)
                with self.assertRaises(ValueError):
                    PrismCalculator.volume(length, width, height)


if __name__ == '__main__':
    unittest.main()
