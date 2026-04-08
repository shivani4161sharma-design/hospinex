import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital.settings')

import django
django.setup()

# Run migrations on cold start so DB tables exist
try:
    from django.core.management import call_command
    call_command('migrate', '--noinput')
except Exception:
    pass

from hospital.wsgi import application
app = application
