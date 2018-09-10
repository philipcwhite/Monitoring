from agent_actions import AgentProcess
import time
import datetime,socket
import agent_settings
import wmi, os,platform
import agent_load

#settings.init()


#a = datetime.datetime.now().second
"""for i in range(0,10000):
    a = datetime.datetime.now().second
    print(a)
    if a == 0:
        agent_process.create_loop()
        print('success')
    time.sleep(1)"""





agent_load.load_config()


#print(agent_settings.config_path)
#print(agent_settings.filename)

AgentProcess.create_loop()

time.sleep(5)
AgentProcess.create_loop()

#time.sleep(5)
#AgentProcess.create_loop()
