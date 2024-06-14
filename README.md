 # BricksLabel

## Overview

This project provides a tool to generate labels from an Excel file and optionally convert them to a Windows executable.

## Requirements

- Python
- Visual Studio Code

## Installation and Setup

### 1. Download and Install Python

1. Go to the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Download the latest version of Python.
3. Run the installer and make sure to check the box that says "Add Python to PATH".
4. Follow the installation steps.

### 2. Download and Install Visual Studio Code (VS Code)

1. Go to the official Visual Studio Code website: [https://code.visualstudio.com/](https://code.visualstudio.com/)
2. Download the latest version of Visual Studio Code.
3. Run the installer and follow the installation steps.

### 3. Clone the Repository

1. Open VS Code.
2. Open the terminal in VS Code by selecting `View > Terminal` or by pressing `` Ctrl+` ``.
3. Clone the repository by running the following command in the terminal:

   git clone https://github.com/DimaDBRK/brickslabel.git

### Set Up a Virtual Environment

Navigate to the cloned repository directory:
cd brickslabel

Create a virtual environment:

python -m venv venv

Activate the virtual environment:
- On Windows: .\venv\Scripts\activate
- On macOS and Linux: source venv/bin/activate

Install the required packages from requirements.txt:
pip install -r requirements.txt

### 5. Run the App

Run the application: 
python app.py

### 6. Convert the Python App to a Windows Executable

Ensure you have PyInstaller installed. If not, install it:
pip install pyinstaller

Use your existing app.spec file to build the executable:
pyinstaller app.spec

The executable will be created in the dist directory.

## Summary
Download and Install: Python and VS Code.
Clone the Repo: Using Git.
Set Up Virtual Environment: python -m venv venv, activate, and install dependencies.
Run the App: python app.py.
Build Executable: Using PyInstaller with app.spec.


