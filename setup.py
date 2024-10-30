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

author="anuranjani",

description="A PyQt5 and PythonOCC based 3D rectangular prism viewer application.",

python_requires=">=3.9",

)