#!/usr/bin/env bash
# Render build script — runs on every deploy.
# Pattern: install deps, collectstatic,migrate, seed data
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Seed the 20 Big Five questions (data.json in backend root)
# || true so re-deploys don't fail if data already exists
python manage.py loaddata data.json || true
