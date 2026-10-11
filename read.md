# DevTrack

DevTrack is a Django-based issue tracking app for managing reporters and issue records.

## App structure

- `issues/` contains the issue-related views and URL configuration.
- `manage.py` starts the Django project.
- `db.sqlite3` is the SQLite database used for local development.

## Available routes

From `issues/urls.py`:

- `reporters/` -> reporters view
- `issues/` -> issues view

## Notes

This project is intended to help track issue reports and associated reporter information in a simple Django application.
