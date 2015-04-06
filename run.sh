#!/bin/sh
python db_create.py
python db_migrate.py
python app.py
