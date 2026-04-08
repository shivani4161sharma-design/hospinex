#!/bin/bash
python -m pip install -r requirements.txt --break-system-packages
python manage.py collectstatic --noinput --clear
python manage.py migrate --noinput
cp -r media staticfiles_build/media
