#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Building the project..."

# Install backend dependencies
pip install -r requirements.txt

# Install frontend dependencies and build the static files
npm install --prefix ../client
npm run build --prefix ../client

# Run database migrations
echo "Running database migrations..."
flask db upgrade

# Run the seed script to populate the database with initial data
echo "Seeding the database..."
python app/seed.py

echo "Migrations and seeding complete."

echo "Build finished."

