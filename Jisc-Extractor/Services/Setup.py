import subprocess
import sys

class Setup:
    def __init__(self, requirements_file='requirements.txt'):
        self.requirements_file = requirements_file
        self.install_packages()

    def install_packages(self):
        try:
            print(f"Installing packages from {self.requirements_file}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", self.requirements_file])
            print("All packages installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while installing packages: {e}")
            print("Please install this requirements manually")
        except FileNotFoundError:
            print(f"Requirements file '{self.requirements_file}' not found.")