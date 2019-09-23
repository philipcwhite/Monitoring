## Run agent as a service

To run the agent at startup using systemd a few changes must be made to the system and files.  

The path variable in agent.py needs to be set to  
path = '/opt/monitoring/agent/' 

We are running under a user named monitoring and storing the application files in /opt/monitoring/.    

sudo mkdir -p /opt/monitoring/agent  
sudo cp agent.py /opt/monitoring/agent/agent.py  
sudo cp settings.ini /opt/monitoring/agent/settings.ini  
sudo chown -R monitoring /opt/monitoring/agent  
sudo chmod -R 755 /opt/monitoring/agent  
  
sudo cp magent.service /lib/systemd/system/magent.service  
sudo chmod 644 /lib/systemd/system/magent.service  
sudo systemctl daemon-reload  
sudo systemctl enable magent.service  
sudo systemctl start magent.service  
