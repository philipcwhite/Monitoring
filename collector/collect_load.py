import os
import collect_settings

def load_config():
    try:
        collect_settings.running = 1 
        f = open(collect_settings.application_path + collect_settings.config_file, "r")
        fl = f.readlines()
        for i in fl:
            if 'server:' in i:
                collect_settings.server = i[7:].replace("\n","")
            if 'port:' in i:
                collect_settings.port = int(i[5:]).replace("\n","")
            if 'secure:' in i:
                collect_settings.secure = i[7:].replace("\n","")
            if 'dbhost:' in i:
                collect_settings.dbhost = i[7:].replace("\n","")
            if 'dbuser:' in i:
                collect_settings.dbuser = i[7:].replace("\n","")
            if 'dbpassword:' in i:
                collect_settings.dbpassword = i[11:].replace("\n","")
            if 'database:' in i:
                collect_settings.database = i[9:].replace("\n","")
    except:
        pass
