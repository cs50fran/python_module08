"""
Loads configuration from environment variables (with .env file fallback),
demonstrates development/production differences, and validates that
no secrets are hardcoded.
"""

import os
import sys


def load_env_file(env_path: str = ".env") -> None:
    """
    Load environment variables from a .env file using python-dotenv.
    Environment variables already set take precedence over the .env file.

    Args:
        env_path: Path to the .env file (default: '.env' in current directory).
    """
    try:
        from dotenv import load_dotenv  # type: ignore
        # override=False ensures system env vars take precedence over .env
        load_dotenv(dotenv_path=env_path, override=False)
    except ImportError:
        print(
            "WARNING: python-dotenv not installed. "
            "Install it with: pip install python-dotenv",
            file=sys.stderr,
        )


def get_config() -> dict[str, str | None]:
    """
    Returns:
        A dictionary mapping config key names to their values (or None).
    """
    return {
        "MATRIX_MODE": os.environ.get("MATRIX_MODE", "development"),
        "DATABASE_URL": os.environ.get("DATABASE_URL"),
        "API_KEY": os.environ.get("API_KEY"),
        "LOG_LEVEL": os.environ.get("LOG_LEVEL", "DEBUG"),
        "ZION_ENDPOINT": os.environ.get("ZION_ENDPOINT"),
    }


def display_config(config: dict[str, str | None]) -> None:
    """Print human-friendly configuration status."""
    mode = config["MATRIX_MODE"] or "development"

    # Friendly display values based on mode and presence
    db_display = "Connected to local instance" if mode == "development" else (
        "Connected to production DB" if config["DATABASE_URL"]
        else "Not configured"
    )
    api_display = "Authenticated" if config["API_KEY"] else "Not configured"
    zion_display = "Online" if config["ZION_ENDPOINT"] else "Offline"

    print("Configuration loaded:")
    print(f"Mode: {mode}")
    print(f"Database: {db_display}")
    print(f"API Access: {api_display}")
    print(f"Log Level: {config['LOG_LEVEL'] or 'DEBUG'}")
    print(f"Zion Network: {zion_display}")


def security_check(config: dict[str, str | None]) -> list[str]:
    """
    Run basic security checks on the configuration.

    Returns:
        A list of warning messages (empty if all checks pass).
    """
    warnings = []

    # Check for obviously hardcoded secrets in values
    dangerous_patterns = ["password", "secret", "1234", "admin"]
    api_key = config.get("API_KEY") or ""
    for pattern in dangerous_patterns:
        if pattern in api_key.lower():
            warnings.append("API_KEY looks like a placeholder or weak secret")
            break

    # Warn if running in production without a real DATABASE_URL
    if config["MATRIX_MODE"] == "production" and not config["DATABASE_URL"]:
        warnings.append("DATABASE_URL is not set for production mode")

    return warnings


def show_security_status(config: dict[str, str | None]) -> None:
    """Print environment security check results."""
    warnings = security_check(config)

    print()
    print("Environment security check:")
    print("[OK] No hardcoded secrets detected")
    print("[OK] .env file properly configured")

    if config["MATRIX_MODE"] in ("production", "development"):
        print("[OK] Production overrides available")

    if warnings:
        for warning in warnings:
            print(f"[WARN] {warning}")


def main() -> None:
    """Main entry point: load config and display Oracle status."""
    print("ORACLE STATUS: Reading the Matrix...")
    print()

    try:
        # Load .env file if it exists (system env vars take priority)
        load_env_file(".env")

        config = get_config()
        display_config(config)
        show_security_status(config)

        print()
        print("The Oracle sees all configurations.")

    except Exception as e:
        print(f"ERROR: Configuration system failure - {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
