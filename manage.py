import os
import sys

def main():
    if os.environ.get('RENDER'):
        os.environ.setdefault(
            "DJANGO_SETTINGS_MODULE",
            "zorpido_config.settings.production"
        )
    else:
        os.environ.setdefault(
            "DJANGO_SETTINGS_MODULE",
            "zorpido_config.settings.local"
        )
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
