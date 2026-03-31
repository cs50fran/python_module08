"""
construct.py - Detect and display Python virtual environment information.

Detects whether the script is running inside a virtual environment,
shows current Python environment details, and provides setup instructions
if no virtual environment is found.
"""

import os
import sys
import site


def is_virtual_env() -> bool:
    # sys.prefix differs from sys.base_prefix when inside a venv
    return sys.prefix != sys.base_prefix


def get_venv_name() -> str | None:
    """Extract the virtual environment name from its path."""
    # use "PATH" if not in venv
    venv_path = os.environ.get("VIRTUAL_ENV")
    if venv_path:
        return os.path.basename(venv_path)
    return None


def get_package_location() -> str:
    """Return the site-packages directory for the current environment."""
    try:
        packages = site.getsitepackages()
        return packages[0] if packages else "Unknown"
    except AttributeError:
        return ("Cannot access env site packages")


def show_outside_venv() -> None:
    """Display information and instructions when not in a venv"""
    print("MATRIX STATUS: You're still plugged in")
    print()
    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: None detected")
    print()
    print("WARNING: You're in the global environment!")
    print("The machines can see everything you install.")
    print()
    print("To enter the construct, run:")
    print("python -m venv matrix_env")
    print("source matrix_env/bin/activate # On Unix")
    print("matrix_env")
    print("Scripts")
    print("activate    # On Windows")
    print()
    print("Then run this program again.")


def show_inside_venv() -> None:
    """Display information when running inside a venv"""
    venv_path = os.environ.get("VIRTUAL_ENV", sys.prefix)
    venv_name = get_venv_name() or os.path.basename(venv_path)
    package_path = get_package_location()

    print("MATRIX STATUS: Welcome to the construct")
    print()
    print(f"Current Python: {sys.executable}")
    print(f"Virtual Environment: {venv_name}")
    print(f"Environment Path: {venv_path}")
    print()
    print("SUCCESS: You're in an isolated environment!")
    print("Safe to install packages without affecting")
    print("the global system.")
    print()
    print("Package installation path:")
    print(package_path)


def main() -> None:
    """Main entry point: detect environment and display appropriate output."""
    try:
        if is_virtual_env():
            show_inside_venv()
        else:
            show_outside_venv()
    except Exception as e:
        print(f"ERROR: Could not detect environment - {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
