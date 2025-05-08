import os

def print_directory_structure(start_path="."):

    for root, dirs, files in os.walk(start_path):
        if '.git' in dirs:
            dirs.remove('.git')

        level = root.replace(start_path, '').count(os.sep)
        indent = ' ' * 4 * level
        print(f"{indent}[{os.path.basename(root)}]")
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            print(f"{sub_indent}{f}")

if __name__ == "__main__":
   
    dir_path = ""
    if not dir_path:
        dir_path = "."
    if not os.path.exists(dir_path):
        print(f"Error: Directory '{dir_path}' not found. Printing current directory instead.")
        dir_path = "."

    print_directory_structure(dir_path)
