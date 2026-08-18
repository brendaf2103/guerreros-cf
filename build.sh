#!/usr/bin/env bash
# Script de construcción para Render (o cualquier hosting compatible con
# "build command"). Se ejecuta automáticamente cada vez que subes cambios.
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate --no-input
