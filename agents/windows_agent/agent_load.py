import agent_settings, agent_sql
import wmi, os, pythoncom


def load_config():
    agent_sql.AgentSQL.create_tables()
    agent_settings.config_path = os.path.join(agent_settings.application_path, agent_settings.config_file)
    agent_settings.thresh_path = os.path.join(agent_settings.application_path, agent_settings.thresh_file)

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
            if 'services:' in i:
                agent_settings.services = i[9:].split(',')
    except:
        pass
    
    """try:
        agent_sql.AgentSQL.delete_thresholds()
        f = open(agent_settings.thresh_path, "r")
        fl = f.readlines()
        for i in fl:
            thresh = i.split(",")
            print(thresh[0], thresh[1], thresh[2], thresh[3], thresh[4])
            agent_sql.AgentSQL.insert_thresholds(thresh[0], thresh[1], thresh[2], thresh[3], thresh[4])
            
    except:
        pass"""
    
    agent_sql.AgentSQL.delete_thresholds()
    f = open(agent_settings.thresh_path, "r")
    fl = f.readlines()
    for i in fl:
        thresh = i.split(",")
        #print(thresh[0], thresh[1], thresh[2], thresh[3], thresh[4])
        agent_sql.AgentSQL.insert_thresholds(thresh[0], thresh[1], thresh[2], thresh[3], thresh[4])

    #print(agent_sql.AgentSQL.select_thresholds)
    #rows=agent_sql.AgentSQL.select_thresholds()
    #for i in rows:
    #    print(i[0])
            
