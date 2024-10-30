# Rectangular Prism Viewer

## Project Overview

This project involves creating a desktop application using PyQt5 that allows users to view and analyze 3D models of rectangular prisms. The application retrieves prism dimensions from a SQLite database, calculates surface area and volume, and displays a 3D CAD model using PythonOCC.

## Installation Instructions

1. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

2. Initialize the SQLite database with sample data:
    ```bash
    python initialize_db.py
    ```

3. Run the application:
    ```bash
    python main.py
    ```

## Usage Guidelines

1. Select a prism designation from the dropdown menu.
2. View the calculated surface area and volume.
3. Click the "Display 3D Model" button to visualize the prism.

## Generating an Executable Installer

To create an executable installer for this project, follow these steps:

1. Install PyInstaller:
    ```bash
    pip install pyinstaller
    ```

2. Run PyInstaller to generate the executable:
    ```bash
    pyinstaller --onefile main.py
    ```

3. The executable will be generated in the `dist` folder. You can distribute this executable to users.

## Additional Information

For more details on PyQt5, refer to the [PyQt5 documentation](https://www.riverbankcomputing.com/static/Docs/PyQt5/).

For more details on PythonOCC, refer to the [PythonOCC documentation](http://www.pythonocc.org/).

