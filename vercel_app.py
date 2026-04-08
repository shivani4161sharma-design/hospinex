import os
import shutil

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital.settings')

import django
django.setup()

# On Vercel, copy the bundled db.sqlite3 to /tmp/ (writable area)
# so all existing data (doctors, departments, etc.) is available
if os.environ.get('VERCEL'):
    src_db = os.path.join(os.path.dirname(__file__), 'db.sqlite3')
    dst_db = '/tmp/db.sqlite3'
    if not os.path.exists(dst_db) and os.path.exists(src_db):
        shutil.copy2(src_db, dst_db)

# Run migrations on cold start
try:
    from django.core.management import call_command
    call_command('migrate', '--noinput')
except Exception:
    pass

from hospital.wsgi import application
app = application
