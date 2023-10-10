#!/usr/bin/bash
sudo apt update
sudo apt install mariadb-server
sudo systemctl start mysql.service
sudo mysql -e "CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin123';"
sudo mysql -e "DROP DATABASE IF EXISTS hustle_db;"
sudo mysql -e "CREATE DATABASE IF NOT EXISTS hustle_db;"
sudo mysql -e "GRANT ALL ON hustle_db.* TO 'admin'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"
sudo mysql < setup/hdb.sql
sudo systemctl restart mysql.service
sudo systemctl status mariadb