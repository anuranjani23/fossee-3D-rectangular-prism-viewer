from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Ax2
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Display.SimpleGui import init_display
from typing import Tuple


def create_rectangular_prism(length: float, width: float, height: float, 
                           origin: Tuple[float, float, float] = (0, 0, 0)) -> object:
    """
    Create a rectangular prism using OpenCASCADE.
    
    Args:
        length (float): Length of the box in X direction
        width (float): Width of the box in Y direction
        height (float): Height of the box in Z direction
        origin (tuple): Origin point coordinates (x, y, z)
    
    Returns:
        object: OpenCASCADE shape object representing the box
    
    Raises:
        ValueError: If any dimension is less than or equal to 0
    """
    # Validate dimensions
    for dim, name in zip([length, width, height], ['length', 'width', 'height']):
        if dim <= 0:
            raise ValueError(f"{name} must be greater than 0")
    
    try:
        # Create origin point
        origin_pnt = gp_Pnt(*origin)
        
        # Create the box using the origin point
        box = BRepPrimAPI_MakeBox(origin_pnt, length, width, height).Shape()
        return box
    
    except Exception as e:
        raise RuntimeError(f"Failed to create box: {str(e)}")


def display_prism(box: object, color: Tuple[float, float, float] = (0.1, 0.5, 0.8)) -> None:
    """
    Display the rectangular prism in a 3D viewer.
    
    Args:
        box (object): OpenCASCADE shape object to display
        color (tuple): RGB color values (0-1 range)
    """
    try:
        # Initialize the display
        display, start_display, add_menu, add_function_to_menu = init_display()
        
        # Create color object
        box_color = Quantity_Color(*color, Quantity_TOC_RGB)
        
        # Display the box with specified color
        display.DisplayShape(box, color=box_color, update=True)
        
        # Set display properties
        display.View_Iso()  # Set isometric view
        display.FitAll()    # Fit view to screen
        
        # Start the display
        start_display()
        
    except Exception as e:
        raise RuntimeError(f"Failed to display box: {str(e)}")


def main():
    """
    Main function to demonstrate the creation and display of a rectangular prism.
    """
    try:
        # Dimensions of the rectangular prism
        length = 40.0
        width = 20.0
        height = 100.0
        origin = (10, 10, 0)  # Starting point offset from (0,0,0)
        color = (0.2, 0.6, 0.9)  # Blue-ish color
        
        print(f"Creating box with dimensions: {length} x {width} x {height}")
        
        # Create the rectangular prism
        box = create_rectangular_prism(
            length=length,
            width=width,
            height=height,
            origin=origin
        )
        
        # Display the rectangular prism
        display_prism(box, color=color)
        
    except ValueError as ve:
        print(f"Invalid input: {str(ve)}")
    except RuntimeError as re:
        print(f"Runtime error: {str(re)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    main()