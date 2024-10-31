# Rectangular Prism Viewer

## Project Overview

The **Rectangular Prism Viewer** is a desktop application built with **PyQt5** that allows users to view and analyze 3D models of rectangular prisms. The application retrieves prism dimensions from a **SQLite** database, calculates the surface area and volume, and displays a 3D CAD model using **PythonOCC**. This project emphasizes software quality through rigorous unit testing and packaging for easy distribution.

## Installation Instructions

To set up the application, follow these steps:

1. **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

2. **Initialize the SQLite database with sample data:**
    ```bash
    python initialize_db.py
    ```

3. **Run the application:**
    ```bash
    python main.py
    ```

## Usage Guidelines

1. **Select a prism designation** from the dropdown menu.
2. **View the calculated surface area and volume**.
3. **Click the "Display 3D Model" button** to visualize the prism.

## Testing Methodology

This application utilizes the built-in Python module `unittest` for automated testing, providing:

- **Test Discovery**: Automatically identifies tests to run.
- **Rich Assertion Methods**: Facilitates various test assertions to ensure code functionality.
- **Test Fixture Support**: Allows setup and teardown of test environments.
- **Subtest Capability**: Supports parameterized testing scenarios.

### Test Structure

The test suite consists of two main classes:

- `TestPrismViewerApp`: Focused on UI and integration tests.
- `TestPrismCalculator`: Concentrated on the core calculation logic.

### Testing Categories

1. **Application Testing**
   - Program initialization
   - UI component verification
   - Database connectivity
   - Window properties

2. **Calculation Testing**
   - Surface area computation
   - Volume computation
   - Edge cases
   - Error handling

## Generating an Executable Installer

To create an executable installer for this project, follow these steps:

1. **Install PyInstaller:**
    ```bash
    pip install pyinstaller
    ```

2. **Run PyInstaller to generate the executable:**
    ```bash
    pyinstaller --onefile main.py
    ```

3. The executable will be generated in the `dist` folder, ready for distribution.

## Packaging Strategy

### Conda Package

The Conda package is structured using a `meta.yaml` file, ensuring proper metadata specification, dependencies, and build requirements are met.

```yaml
package:
  name: prism_viewer
  version: 0.1.0

requirements:
  build:
    - python =3.8
    - {{ compiler('cxx') }}
  host:
    - python =3.8
    - pip
    - setuptools
    - numpy =1.22.4
    - swig
    - pythonocc-core =7.8.1
```
### PIP Project

The PIP package is implemented with a setup.py file that includes necessary metadata and requirements.

```py
from setuptools import setup, find_packages

setup(
    name="prism-viewer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "PyQt5",
        "numpy",
        "OCC-Core",
    ],
    entry_points={
        'console_scripts': [
            'prism-viewer=main:main',
        ],
    },
    python_requires=">=3.8",
)
```
### Build and Test Execution Steps

Environment Setup:

```bash
docker build -t rectangular_prism_viewer .
```

Test Execution:

```bash
python -m unittest discover -v
```


