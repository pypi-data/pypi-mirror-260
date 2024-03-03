# Don't delete or rename this file because pyproject.toml needs it.

# local libraries
try:
    # attempt relative import (assuming running as part of a package)
    from .main import main
except ImportError:
    # fallback to absolute import (assuming running as standalone script)
    from main import main

if __name__ == "__main__":
    main()
