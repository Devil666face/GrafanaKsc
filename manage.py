#!/usr/bin/env python
def init_django():
    import django
    from pathlib import Path
    from django.conf import settings

    BASE_DIR = Path(__file__).resolve().parent

    if settings.configured:
        return

    settings.configure(
        INSTALLED_APPS=[
            'db',
        ],
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        },
        # DATETIME_FORMAT = '%d-%m-%Y %H:%M:%S',
        # USE_TZ = True,
        # TIME_ZONE = 'Europe/Moscow'
    )
    django.setup()


if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    init_django()
    execute_from_command_line()
