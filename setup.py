import os
import subprocess
from setuptools import setup, find_packages

def install_rustscan():
    # Download RustScan .deb package
    print("Downloading RustScan .deb package...")
    deb_url = "https://github.com/RustScan/RustScan/releases/download/2.0.1/rustscan_2.0.1_amd64.deb"
    deb_filename = "rustscan_2.0.1_amd64.deb"

    # Download RustScan using wget
    subprocess.check_call(['wget', deb_url, '-O', deb_filename])

    # Install the .deb package using dpkg
    print("Installing RustScan...")
    subprocess.check_call(['sudo', 'dpkg', '-i', deb_filename])

    # Fix dependencies if any are missing
    subprocess.check_call(['sudo', 'apt-get', 'install', '-f'])

    # Clean up the downloaded .deb file
    os.remove(deb_filename)
    print("RustScan installation complete.")

def install_nmap():
    # Install nmap via apt
    print("Installing nmap...")
    subprocess.check_call(['sudo', 'apt-get', 'install', '-y', 'nmap'])
    print("nmap installation complete.")

def install_requirements():
    # Install Python requirements
    print("Installing Python requirements...")
    subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])
    print("Python requirements installation complete.")

def create_binary():
    # Use pyinstaller to create a binary from mynmap.py
    print("Creating binary from mynmap.py...")
    subprocess.check_call(['pyinstaller', '--onefile', '--name', 'mynmap', 'mynmap.py'])
    print("Binary creation complete.")

    # Move binary to user binaries directory
    binary_path = os.path.join(os.getcwd(), 'dist', 'mynmap')
    if os.path.exists(binary_path):
        subprocess.check_call(['sudo', 'mv', binary_path, '/usr/local/bin/mynmap'])
        print("Binary moved to /usr/local/bin/mynmap.")
    else:
        print("Error: Binary not found after PyInstaller build.")

def main():
    # Install all dependencies and create binary
    install_rustscan()
    install_nmap()
    install_requirements()
    create_binary()

# Call the main function
if __name__ == '__main__':
    main()

# Setuptools configuration for the package
setup(
    name='mynmap',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # Python requirements are included in requirements.txt
    ],
    entry_points={
        'console_scripts': [
            'mynmap = mynmap:main',  # Adjust based on your package structure
        ],
    },
)
