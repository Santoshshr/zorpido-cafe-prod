"""Legacy settings module (deprecated).

This project uses a settings package (zorpido_config.settings) with
`base.py`, `local.py`, and `production.py`. Importing this file is
deprecated and may cause configuration conflicts.

To prevent accidental usage, importing this module raises an ImportError
explaining the correct settings modules to use.

Why: having both a module and a package named ``settings`` can lead to
ambiguous imports and unexpected behavior in production. This replacement
ensures the package-based configuration is authoritative.
"""

raise ImportError(
    "zorpido_config.settings (legacy) has been disabled. Use the settings package:\n"
    "- Local development: zorpido_config.settings.local\n"
    "- Production: zorpido_config.settings.production\n"
    "Set the DJANGO_SETTINGS_MODULE environment variable accordingly."
)