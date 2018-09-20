import os
import collect_settings

def load_config():
    try:
        collect_settings.running = 1 
        f = open(collect_settings.application_path + collect_settings.config_file, "r")
        fl = f.readlines()
        for i in fl:
            if 'server:' in i:
                collect_settings.server = i[7:]
            if 'port:' in i:
                collect_settings.port = int(i[5:])
            if 'secure:' in i:
                collect_settings.secure = i[7:]
    except:
        pass