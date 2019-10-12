## Run agent as a service

The magent shell script will copy the agent.py and settings.ini file to /opt/monitoring/agent.  It will create the user monitoring to run the script as a service.  And lastly it will create the magent.service file and register it with systemd.  The script uses Python 3.7.  If your version is different you will have to change the script to your version.  I have only tested with 3.7.  It will probably work back to 3.6.
