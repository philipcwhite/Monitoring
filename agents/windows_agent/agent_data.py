import os
import socket
import platform
import time
import agent_settings, agent_sql, agent_windows

class AgentData():
    def data_process():
        # Set time
        agent_time = str(time.time()).split('.')[0]
        # Get Hostname
        name = agent_settings.name
        # Configuration
        try:
            osplatform = platform.system()
            osarchitecture = platform.architecture()[0]
            osbuild = platform.win32_ver()[1]
            ipaddress = socket.gethostbyname(socket.gethostname())
            domain = socket.getfqdn().split('.', 1)[1]
            processors = str(os.cpu_count())
            agent_sql.AgentSQL.insert_agentdata(agent_time, name, 'conf.os.name', osplatform)
            agent_sql.AgentSQL.insert_agentdata(agent_time, name, 'conf.os.architecture', osarchitecture)
            agent_sql.AgentSQL.insert_agentdata(agent_time, name, 'conf.os.build', osbuild)
            agent_sql.AgentSQL.insert_agentdata(agent_time, name, 'conf.ipaddress', ipaddress)
            agent_sql.AgentSQL.insert_agentdata(agent_time, name, 'conf.domain', domain)
            agent_sql.AgentSQL.insert_agentdata(agent_time, name, 'conf.processors', processors)
            if osplatform == "Windows":
                agent_windows.AgentWindows.data_windows(agent_time, name)
            else:
                # Possible other platforms
                pass
        except:
            pass
        output = agent_sql.AgentSQL.select_agent_data()
        return output
