import os
import event_settings,event_available

def load_config():
    try:
        event_settings.running = 1 
        f = open(event_settings.application_path + event_settings.config_file, "r")
        fl = f.readlines()
        for i in fl:
            if 'mon_server:' in i:
                event_settings.server = i[11:].replace("\n","")
            if 'mon_port:' in i:
                event_settings.port = int(i[9:].replace("\n",""))
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
            if 'mailactive:' in i:
                event_settings.mailactive = int(i[11:].replace("\n",""))
            if 'mailserver:' in i:
                event_settings.mailserver = i[11:].replace("\n","")
            if 'mailadmin:' in i:
                event_settings.mailadmin = i[10:].replace("\n","")
            if 'availability_check:' in i:
                event_settings.availability_check = int(i[19:].replace("\n",""))
            if 'availability_severity:' in i:
                event_settings.availability_severity = i[22:].replace("\n","")
    except:
        pass
