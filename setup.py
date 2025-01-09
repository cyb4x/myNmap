import os
import subprocess
from setuptools import setup, find_packages

def check_if_installed(command):
    """Check if a command is installed on the system."""
    try:
        subprocess.check_output([command, '--version'], stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False


def install_nmap():
    """Install nmap if not already installed."""
    if not check_if_installed('nmap'):
        print("Installing nmap...")
        subprocess.check_call(['sudo', 'apt-get', 'install', '-y', 'nmap'])
        print("nmap installation complete.")
    else:
        print("nmap is already installed.")

def install_python_requirements():
    """Force install Python requirements."""
    print("Installing Python requirements...")
    pip_install_cmd = [
        'sudo', 'pip', 'install',
        '--upgrade', 'pyinstaller', 'pyinstaller-hooks-contrib',
        '--break-system-packages', '--root-user-action=ignore'
    ]
    
    # Install basic requirements
    subprocess.check_call(pip_install_cmd)

    # Check and install requirements from requirements.txt
    if os.path.exists('requirements.txt'):
        pip_install_cmd = [
            'sudo', 'pip', 'install', '-r', 'requirements.txt',
            '--break-system-packages', '--root-user-action=ignore'
        ]
        subprocess.check_call(pip_install_cmd)

    print("Python requirements installation complete.")

def create_binary():
    """Create the binary using PyInstaller."""
    print("Creating binary from mynmap.py...")
    subprocess.check_call(['pyinstaller', '--onefile', '--name', 'mynmap', 'mynmap.py'])
    print("Binary creation complete.")

    binary_path = os.path.join(os.getcwd(), 'dist', 'mynmap')
    if os.path.exists(binary_path):
        subprocess.check_call(['sudo', 'mv', binary_path, '/usr/local/bin/mynmap'])
        print("Binary moved to /usr/local/bin/mynmap.")
    else:
        print("Error: Binary not found after PyInstaller build.")

def main():
    """Run the setup process."""
    install_nmap()
    install_python_requirements()
    create_binary()

if __name__ == '__main__':
    main()

setup(
    name='mynmap',
    version='0.2',
    packages=find_packages(),
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'mynmap = mynmap:main',
        ],
    },
)
