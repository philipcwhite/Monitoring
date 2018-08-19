import agent_settings
import wmi, os, pythoncom

def load_config():
    """try:
        pythoncom.CoInitialize()
        c = wmi.WMI()
        for i in c.Win32_Service(Name='AgentService'):
            agent_settings.application_path = i.PathName
            agent_settings.application_path = agent_settings.application_path.replace('\\','/')
            agent_settings.application_path = agent_settings.application_path.replace('\"','')
            agent_settings.application_path = agent_settings.application_path.replace('agent_service.exe','')
    except:
        pass"""


    agent_settings.config_path = os.path.join(agent_settings.application_path, agent_settings.filename)


    # Load configuration
    try:
        f = open(agent_settings.config_path, "r")
        fl = f.readlines()
        for i in fl:
            if 'server:' in i:
                agent_settings.server = i[7:]
            if 'port:' in i:
                agent_settings.port = int(i[5:])
            if 'secure:' in i:
                agent_settings.secure = i[7:]
            if 'log:' in i:
                agent_settings.log = i[4:]
            if 'servicemon:' in i:
                agent_settings.servicemon = i[11:].split(',')
    except:
        pass