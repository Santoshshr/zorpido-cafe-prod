try:
    # Default to production settings when imported (suitable for Render)
    from .production import *  # noqa: F401,F403
except Exception:
    # Fall back to local settings when production is not available (developer machines)
    try:
        from .local import *  # noqa: F401,F403
    except Exception:
        # If neither import works, leave module namespace empty and allow importing code
        # to handle configuration errors explicitly.
        pass
# Default to production settings when the package is imported in runtime
# This ensures services (Render) that import `zorpido_config.settings`
# receive the production configuration. Fall back to local for
# developer machines or where production settings fail to import.

