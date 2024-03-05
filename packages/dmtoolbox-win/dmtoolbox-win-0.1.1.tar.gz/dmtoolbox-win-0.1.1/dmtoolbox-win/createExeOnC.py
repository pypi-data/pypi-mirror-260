import os
import sys

# Functions
__all__ = ['is_installed', 'install']

# Variables
__all__ += []

def is_installed(destination, filename):
    # Checks if the file exists in the destination directory
    full_path = os.path.join(destination, filename)
    return os.path.exists(full_path)

def install():
    destination = 'C:\\Program Files\\DM File Explorer'
    filename = 'DMFileExplorerAssist.exe'

    # Checks if the program is already installed
    if is_installed(destination, filename):
        print("The program is already installed.")
        return

    # Creates the destination directory if it does not exist
    if not os.path.exists(destination):
        os.makedirs(destination)

    # Gets the path of the currently running executable
    current_executable = sys.executable
    print(f"==>> sys.executable: {sys.executable}")

    # # Copies the current executable to the destination
    # shutil.copyfile(current_executable, os.path.join(destination, filename))

    # print("Installation completed successfully.")


if __name__ == "__main__":
    print("This module should not be run directly.")
