from pathlib import Path
import re


def windows_path_to_wsl(windows_path):
    # This regex checks for patterns like C:\something or C:/something
    if re.match(r"[a-zA-Z]:[/\\]", windows_path):
        # Convert Windows drive letter to WSL mount point
        drive, path_part = windows_path.split(':', 1)
        path_part = path_part.replace('\\', '/')
        wsl_path = f"/mnt/{drive.lower()}{path_part}"
        return wsl_path
    return windows_path


def is_windows_path(path):
    return '\\' in path or re.match(r"[a-zA-Z]:[/\\]", path)


def handle_path(user_input_path):
    if is_windows_path(user_input_path):
        print("Detected Windows path. Converting...")
        return windows_path_to_wsl(user_input_path)
    return user_input_path


def create_file_path(base_directory, user_input_filename):
    """
    Constructs a safe and absolute file path using a sanitized base directory and user input filename.

    Args:
    base_directory (str): The base directory path which will be sanitized and used.
    user_input_filename (str): The filename provided by the user, which needs to be sanitized.

    Returns:
    str: The absolute path to the file within the sanitized base directory.
    """
    base_directory = handle_path(base_directory)
    # Sanitize base directory by resolving any relative paths to absolute and removing any unnecessary parts
    sanitized_base = Path(base_directory).resolve()

    # Sanitize the filename to ensure it is just a filename without path components
    sanitized_filename = Path(user_input_filename).name

    # Combine the sanitized base directory with the sanitized filename using the '/' operator
    full_path = sanitized_base / sanitized_filename

    return str(full_path)
