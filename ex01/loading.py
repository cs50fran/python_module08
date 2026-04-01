import os
import sys
import importlib


def check_dependency(p_n: str, import_name: str | None = None
                     ) -> tuple[bool, str]:
    """
    Check if a package is installed and return its version.

    Args:
        p_n: The pip package name (used for display).
        import_name: The import name if different from package_name.

    Returns:
        A tuple of (is_available, version_string).
    """
    name = import_name or p_n
    try:
        module = importlib.import_module(name)
        version = getattr(module, "__version__", "unknown")
        return True, version
    except ImportError:
        return False, "not installed"


def check_all_dependencies() -> dict[str, tuple[bool, str]]:
    """Check all required dependencies and return their status."""
    deps = {
        "pandas": ("pandas", None),
        "numpy": ("numpy", None),
        "matplotlib": ("matplotlib", None),
    }
    results = {}
    for display_name, (pkg, imp) in deps.items():
        available, version = check_dependency(pkg, imp)
        results[display_name] = (available, version)
    return results


def show_dependency_status(results: dict[str, tuple[bool, str]]) -> bool:
    """ True if all required deps are available, False otherwise """
    print("Checking dependencies:")
    all_ok = True
    labels = {
        "pandas": "Data manipulation",
        "numpy": "Numerical computation",
        "matplotlib": "Visualization",
    }
    for name, (available, version) in results.items():
        label = labels.get(name, name)
        if available:
            print(f"[OK] {name} ({version}) - {label} ready")
        else:
            print(f"[MISSING] {name} - {label} not available")
            all_ok = False
    return all_ok


def show_missing_instructions() -> None:
    """Print instructions to install missing dependencies."""
    print()
    print("Some dependencies are missing. Install them with:")
    print()
    print("  Using pip:")
    print("    pip install -r requirements.txt")
    print()
    print("  Using Poetry:")
    print("    poetry install")


def analyze_matrix_data() -> None:
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, "matrix_analysis.png")

    print()
    print("Analyzing Matrix data...")

    n_points = 1000
    print(f"Processing {n_points} data points...")

    data = np.random.randn(n_points)
    np.random.uniform(0, 1000, n_points)
    data_frame = pd.DataFrame(data, columns=["signal"])

    total = data_frame["signal"].sum()
    print(f"  Sum: {total:.4f}")
    print("Generating visualization...")

    data_frame["signal"].plot(title=f"Matrix Signal (sum={total:.4f})")
    plt.axhline(total, color="red", linestyle="--", label=f"Sum: {total:.4f}")
    plt.legend()
    plt.savefig(output_file)
    plt.close()

    print()
    print("Analysis complete!")
    print(f"Results saved to: {output_file}")


def main() -> None:
    print()
    print("LOADING STATUS: Loading programs...")
    print()

    results = check_all_dependencies()
    all_ok = show_dependency_status(results)

    if not all_ok:
        show_missing_instructions()
        sys.exit(1)

    try:
        analyze_matrix_data()
    except Exception as e:
        print(f"ERROR: Analysis failed - {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()


"""
poetry install
poetry run
"""
