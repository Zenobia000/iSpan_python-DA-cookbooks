"""
Helper functions for the Python OOP course.

This module contains utility functions used across the course examples.
"""

import os
import sys
import datetime
from pathlib import Path


def get_project_root():
    """
    Find the project root directory.
    
    Returns:
        pathlib.Path: Path to the project root directory
    """
    # Strategy 1: Using __file__ (when running as script)
    if '__file__' in globals():
        file_path = Path(__file__).resolve()
        # Look for a marker file/directory
        for parent in [file_path, *file_path.parents]:
            if (parent / 'requirements.txt').exists() or (parent / 'setup.py').exists():
                return parent
                
    # Strategy 2: Using current working directory (when running in Jupyter)
    current_dir = Path(os.getcwd()).resolve()
    for parent in [current_dir, *current_dir.parents]:
        if (parent / 'requirements.txt').exists() or (parent / 'setup.py').exists():
            return parent
            
    # Fallback: Return current directory
    return current_dir


def create_timestamp(include_time=True):
    """
    Create a formatted timestamp string.
    
    Args:
        include_time (bool): Whether to include time in the timestamp
    
    Returns:
        str: Formatted timestamp
    """
    now = datetime.datetime.now()
    if include_time:
        return now.strftime("%Y-%m-%d %H:%M:%S")
    return now.strftime("%Y-%m-%d")


def format_output(title, content, width=80):
    """
    Format content with a title and border for console output.
    
    Args:
        title (str): The title text
        content (str or list): The content text or list of lines
        width (int): Width of the output box
    
    Returns:
        str: Formatted output string
    """
    result = []
    border = "=" * width
    
    result.append(border)
    result.append(f"| {title.center(width - 4)} |")
    result.append(border)
    
    if isinstance(content, list):
        for line in content:
            result.append(f"| {str(line):<{width-4}} |")
    else:
        result.append(f"| {str(content):<{width-4}} |")
    
    result.append(border)
    return "\n".join(result)


def add_to_python_path(directory):
    """
    Add a directory to the Python path.
    
    Args:
        directory (str or pathlib.Path): Directory to add to Python path
    
    Returns:
        bool: True if added successfully, False if already in path
    """
    directory = str(directory)
    if directory not in sys.path:
        sys.path.insert(0, directory)
        return True
    return False


if __name__ == "__main__":
    # Example usage
    project_root = get_project_root()
    print(f"Project root: {project_root}")
    
    timestamp = create_timestamp()
    print(f"Current timestamp: {timestamp}")
    
    example_output = format_output(
        "Example Output",
        ["This is a formatted output example", "With multiple lines"]
    )
    print(example_output) 