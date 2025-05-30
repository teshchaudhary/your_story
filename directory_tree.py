import os

def print_directory_structure(start_path='.', indent=''):
    for item in os.listdir(start_path):
        item_path = os.path.join(start_path, item)
        print(indent + '|-- ' + item)
        if os.path.isdir(item_path):
            print_directory_structure(item_path, indent + '    ')

if __name__ == '__main__':
    print("Directory structure of current directory:\n")
    print_directory_structure()
