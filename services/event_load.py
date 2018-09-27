import os
import event_settings

def load_config():
    try:
        event_settings.running = 1 
        f = open(event_settings.application_path + event_settings.config_file, "r")
        fl = f.readlines()
        for i in fl:
            if 'server:' in i:
                event_settings.server = i[7:].replace("\n","")
            if 'port:' in i:
                event_settings.port = int(i[5:]).replace("\n","")
            if 'secure:' in i:
                event_settings.secure = i[7:].replace("\n","")
            if 'dbhost:' in i:
                event_settings.dbhost = i[7:].replace("\n","")
            if 'dbuser:' in i:
                event_settings.dbuser = i[7:].replace("\n","")
            if 'dbpassword:' in i:
                event_settings.dbpassword = i[11:].replace("\n","")
            if 'database:' in i:
                event_settings.database = i[9:].replace("\n","")
    except:
        pass
