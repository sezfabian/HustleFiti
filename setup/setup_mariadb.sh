#!/usr/bin/bash
sudo apt update
sudo apt install mariadb-server
sudo mysql_secure_installation
sudo mariadb -e "CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin123';"
sudo mariadb -e "GRANT ALL ON *.* TO 'admin'@'localhost' IDENTIFIED BY 'admin123' WITH GRANT OPTION;"
sudo mariadb -e "FLUSH PRIVILEGES;"
sudo systemctl status mariadb