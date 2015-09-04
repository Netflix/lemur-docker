#!/bin/bash

echo "Changing postgres password..."
sudo -u postgres psql -h postgres --command "CREATE USER lemur with PASSWORD 'lemur';"
echo "Done changing postgres password..."
echo "Creating lemurdb....."
sudo -u lemur createdb -h postgres -O postgres lemur
echo "DONE CREATING lemurdb..."

cd /usr/local/src/lemur/lemur
python manage.py create_config
python manage.py init -p password
python manage.py start -w 6 -b 0.0.0.0:8000
