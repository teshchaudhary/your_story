import os

def print_directory_structure(start_path="."):
    """
    Prints the directory structure starting from the given path.

    Args:
        start_path (str, optional): The path to start printing from. Defaults to the current directory.
    """
    for root, dirs, files in os.walk(start_path):
        level = root.replace(start_path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(f"{indent}[{os.path.basename(root)}]")
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            print(f"{sub_indent}{f}")

if __name__ == "__main__":
    # Get the directory path from the user, default to current directory if input is invalid
    dir_path = input("Enter the directory path to print its structure (or press Enter for current directory): ").strip()
    if not dir_path:
        dir_path = "."  # Use current directory
    if not os.path.exists(dir_path):
        print(f"Error: Directory '{dir_path}' not found.  Printing current directory instead.")
        dir_path = "."

    print_directory_structure(dir_path)
