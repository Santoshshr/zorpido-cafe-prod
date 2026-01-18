# Default to production settings when the package is imported in runtime
# This ensures services (Render) that import `zorpido_config.settings`
# receive the production configuration. Fall back to local for
# developer machines or where production settings fail to import.
try:
	from .production import *
except Exception:
	from .local import *
