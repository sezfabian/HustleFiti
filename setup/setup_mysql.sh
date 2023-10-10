#!/usr/bin/bash
wget https://dev.mysql.com/get/mysql-apt-config_0.8.12-1_all.deb
sudo dpkg -i mysql-apt-config_0.8.12-1_all.deb
sudo apt update
sudo systemctl start mysql.service
sudo mysql -e "CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin123';"
sudo mysql -e "DROP DATABASE IF EXISTS hustle_db;"
sudo mysql -e "CREATE DATABASE IF NOT EXISTS hustle_db;"
sudo mysql -e "GRANT ALL ON hustle_db.* TO 'admin'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"
sudo mysql < setup/hdb.sql
sudo systemctl restart mysql.service
