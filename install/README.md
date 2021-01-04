#Readme

Installing the server is fairly straight forward.

Install Python
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.8 python3-pip python3.8-dev python3.8-venv

MySQL
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
sudo mysql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
FLUSH PRIVILEGES;
SELECT user,authentication_string,plugin,host FROM mysql.user;
GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' IDENTIFIED BY 'password';
exit

MySQL add monitoring user
CREATE USER 'monitoring'@'localhost' IDENTIFIED BY 'password';
GRANT ALL ON monitoring.* TO 'monitoring'@'localhost';

While logged in to mysql run the database/monitoring.sql script to create the database.

To install theserver components
chmod 755 mserver
sudo ./mserver

If you changed your password, you may need to modify the user parameters in 
web/model.py
services/collect.py
services/event.py

Passowrds for collect and event.py should be picked up by settings.ini but there may be issues in this early release.

#Installing the agent
The agent is in the folder agents/linux.
sudo chmod 755 magent
./magent
