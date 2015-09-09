#!/bin/bash

echo "Creating lemurdb..."
sudo -u postgres psql -h postgres --command "CREATE DATABASE lemur;"
echo "Creating the lemur user..."
sudo -u postgres psql -h postgres --command "CREATE USER lemur WITH PASSWORD 'lemur';"
echo "Changing postgres password..."
sudo -u postgres psql -h postgres --command "GRANT ALL PRIVILEGES ON DATABASE lemur to lemur;"
echo "Done changing postgres password..."
echo "DONE CREATING lemurdb..."

cd /usr/local/src/lemur/lemur
python manage.py init -p password
python manage.py start -w 6 -b 0.0.0.0:8000
