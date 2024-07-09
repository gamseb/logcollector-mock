#!/bin/bash

# Check if the script received an argument
if [ -z "$1" ]; then
    echo "Usage: $0 <path_to_python_script>"
    exit 1
fi

# Get the path to the Python script
PYTHON_SCRIPT=$1

# Check if the specified file exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "Error: File '$PYTHON_SCRIPT' not found!"
    exit 1
fi

# Get the base name of the Python script (without extension)
SCRIPT_NAME=$(basename "$PYTHON_SCRIPT" .py)

# Create a virtual environment
python -m venv build_env

# Activate the virtual environment
source build_env/bin/activate

# Install PyInstaller in the virtual environment
pip install pyinstaller

# Run PyInstaller to build the executable for 64-bit Windows
pyinstaller --onefile --platform "win64" --name "$SCRIPT_NAME.exe" "$PYTHON_SCRIPT"

# Deactivate the virtual environment
deactivate

# Check if the build was successful
if [ -f "dist/$SCRIPT_NAME.exe" ]; then
    echo "Build successful. Executable is located in the 'dist' directory."
else
    echo "Build failed."
    exit 1
fi

# Clean up
rm -rf build "$SCRIPT_NAME.spec" venv

echo "Done."