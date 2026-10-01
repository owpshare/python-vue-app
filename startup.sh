#!/bin/bash
set -e
rm -rf /home/site/wwwroot/backend
mkdir -p /home/site/wwwroot/backend/database
cp -a dist /home/site/wwwroot/ 
gunicorn --bind=0.0.0.0 --timeout 600 app:app