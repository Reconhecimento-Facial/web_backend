#!/bin/sh

poetry run alembic upgrade head

poetry run fastapi dev ./web_backend/app.py