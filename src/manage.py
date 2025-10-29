#!/usr/bin/env python
import os
import sys
import asyncio
import django

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django.") from exc

    django.setup()

    if 'createadmin' in sys.argv:
        from django.contrib.auth.models import User
        if not User.objects.filter(username="superadmin").exists():
            User.objects.create_superuser(
                username="superadmin",
                password="superadmin02",
                email="admin@example.com",
            )
            print("✅ Superuser 'superadmin' created successfully!")
        else:
            print("⚠️  Superuser 'superadmin' already exists.")
        return 
    
    if 'runbot' in sys.argv:
        from .telegram_bot import main
        asyncio.run(main())
        return

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
