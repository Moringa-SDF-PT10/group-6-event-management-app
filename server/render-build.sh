#!/usr/bin/env bash

set -o errexit

echo "Building the project..."


pip install -r requirements.txt


npm install --prefix ../client
npm run build --prefix ../client


export FLASK_APP="app:create_app()"


echo "Running database migrations..."
flask db upgrade


echo "Seeding the database..."
python app/seed.py

echo "Migrations and seeding complete."

echo "Build finished."

