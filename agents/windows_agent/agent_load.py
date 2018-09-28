import agent_settings, agent_sql
import socket

def load_config():
    #Set name and create SQL database
    try:
        agent_settings.name = socket.gethostname().lower()
        agent_sql.AgentSQL.create_tables()
    except:
        pass

    # Load configuration
    try:
        f = open(agent_settings.application_path + "settings.cfg", "r")
        fl = f.readlines()
        for i in fl:
            if 'server:' in i:
                agent_settings.server = i[7:].replace("\n","")
            if 'port:' in i:
                agent_settings.port = int(i[5:].replace("\n",""))
            if 'secure:' in i:
                agent_settings.secure = int(i[7:].replace("\n",""))
            if 'log:' in i:
                agent_settings.log = i[4:].replace("\n","")
            if 'services:' in i:
                agent_settings.services = i[9:].replace("\n","").split(',')
    except:
        pass

    # Load thresholds    
    try:
        agent_sql.AgentSQL.delete_thresholds()
        f = open(agent_settings.application_path + "thresholds.cfg", "r")
        fl = f.readlines()
        for i in fl:
            thresh = i.split(",")
            agent_sql.AgentSQL.insert_thresholds(thresh[0], thresh[1], thresh[2], thresh[3], thresh[4])
    except:
        pass

