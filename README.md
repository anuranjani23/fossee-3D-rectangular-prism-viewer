Here's an updated `README.md` to reflect the latest details and ensure compatibility with Python 3.11 and the project's environment setup.

---

# Rectangular Prism Viewer

## Project Overview

The **Rectangular Prism Viewer** is a desktop application developed in **PyQt5** that enables users to view, analyze, and interact with 3D models of rectangular prisms. The application retrieves prism dimensions from a **SQLite** database, calculates surface area and volume, and displays a detailed 3D CAD model using **PythonOCC**. This project prioritizes software quality through unit testing and packaging for easy deployment and distribution.

## Installation Instructions

To set up the application environment, follow these steps:

1. **Create and activate a Conda environment with the required dependencies:**
    ```bash
    conda env create -f environment.yml
    conda activate prism_viewer_env
    ```

2. **Initialize the SQLite database with sample data:**
    ```bash
    python initialize_db.py
    ```

3. **Run the application:**
    ```bash
    prism_viewer  # or `python -m prism_viewer.main` if not configured
    ```

## Usage Guidelines

1. **Select a prism designation** from the dropdown menu in the main application window.
2. **View the calculated surface area and volume** for the selected prism.
3. **Click "Display 3D Model"** to visualize the prism model in a 3D interactive view.

## Testing Methodology

This application employs Python's `unittest` framework for automated testing. This framework provides:

- **Test Discovery**: Automatically finds tests to execute.
- **Assertion Methods**: Verifies expected outputs at various stages.
- **Fixture Support**: Manages setup and teardown for each test.
- **Subtest Support**: Facilitates parameterized testing to handle a variety of cases.

### Test Structure

The test suite comprises two main classes:

- `TestPrismViewerApp`: Focused on user interface and application integration tests.
- `TestPrismCalculator`: Ensures the accuracy and reliability of the core prism calculations.

### Testing Categories

1. **Application Testing**
   - Initialization of the main application
   - Verification of UI components
   - Database connectivity
   - Window properties and behaviors

2. **Calculation Testing**
   - Correctness of surface area and volume computations
   - Handling of edge cases
   - Error handling for invalid inputs

## Generating an Executable Installer

To create a standalone executable installer:

1. **Install PyInstaller** (if not already in your environment):
    ```bash
    pip install pyinstaller
    ```

2. **Use PyInstaller to generate the executable:**
    ```bash
    pyinstaller --onefile prism_viewer/main.py
    ```

3. The executable will be created in the `dist` folder and will be ready for distribution.

## Packaging Strategy

### Conda Package

The Conda package is defined in `meta.yaml`, specifying dependencies and metadata to facilitate reproducible environment creation. Below is a sample of the configuration:

```yaml
package:
  name: prism_viewer
  version: 0.1.1

requirements:
  build:
    - python=3.11
    - {{ compiler('cxx') }}
  host:
    - python=3.11
    - pip
    - setuptools
    - numpy=1.26.4
    - swig
    - pythonocc-core=7.8.1
  run:
    - python=3.11
    - pyqt=5.15.9
    - sqlite
    - six=1.16.0
    - svgwrite
```

### PIP Project

The PIP package is configured using `setup.py`, which includes necessary metadata and requirements. Below is a sample `setup.py`:

```python
from setuptools import setup, find_packages

setup(
    name="prism-viewer",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "PyQt5==5.15.9",
        "numpy==1.26.4",
        "pythonocc-core==7.8.1",
        "six==1.16.0",
        "svgwrite",
    ],
    entry_points={
        'console_scripts': [
            'prism_viewer=prism_viewer.main:main',
        ],
    },
    python_requires=">=3.11",
)
```

### Build and Test Execution Steps

#### Docker Setup

To build the application in a Docker container:

```bash
docker build -t rectangular_prism_viewer .
```

#### Running Tests

Execute the test suite to ensure functionality:

```bash
python -m unittest discover -v
```

#### Conda Environment Setup

This project is designed to run in a **Conda environment with Python 3.11**. Make sure to use the provided `environment.yml` file for an easy setup:

```bash
conda env create -f environment.yml
conda activate prism_viewer_env
```

---
