import os, smtplib, datetime, time, pymysql.cursors
from email.message import EmailMessage

class EventSettings:
    application_path = 'C:\\Progra~1\\monitoring\\event\\'
    availability_check = 300
    availability_severity = 1
    config_file = "settings.cfg"
    database = "monitoring"
    dbhost = "localhost"
    dbpassword = "test"
    dbuser = "test"
    mailactive = 0
    mailadmin = "monitoring@monitoring"
    mailserver = "localhost"
    running = 1

class EventConfig:
    def load_config():
        try:
            EventSettings.running = 1 
            f = open(EventSettings.application_path + EventSettings.config_file, "r")
            fl = f.readlines()
            for i in fl:
                if 'mon_server:' in i: EventSettings.server = i[11:].replace("\n","")
                if 'mon_port:' in i :EventSettings.port = int(i[9:].replace("\n",""))
                if 'dbhost:' in i: EventSettings.dbhost = i[7:].replace("\n","")
                if 'dbuser:' in i: EventSettings.dbuser = i[7:].replace("\n","")
                if 'dbpassword:' in i: EventSettings.dbpassword = i[11:].replace("\n","")
                if 'database:' in i: EventSettings.database = i[9:].replace("\n","")
                if 'mailactive:' in i: EventSettings.mailactive = int(i[11:].replace("\n",""))
                if 'mailserver:' in i: EventSettings.mailserver = i[11:].replace("\n","")
                if 'mailadmin:' in i: EventSettings.mailadmin = i[10:].replace("\n","")
                if 'availability_check:' in i: EventSettings.availability_check = int(i[19:].replace("\n",""))
                if 'availability_severity:' in i: EventSettings.availability_severity = i[22:].replace("\n","")
        except: pass

class EventData:
    def mon_con():
        connection = pymysql.connect(host = EventSettings.dbhost,
                                     user = EventSettings.dbuser,
                                     password = EventSettings.dbpassword,
                                     db = EventSettings.database,
                                     charset = 'utf8mb4',
                                     cursorclass = pymysql.cursors.DictCursor)
        return connection

    def agent_select_id():
        connection = EventData.mon_con()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT id from agentevents ORDER BY id DESC LIMIT 1" 
                cursor.execute(sql)
                result = cursor.fetchone()
                result = str(result["id"])
                return result
        finally: connection.close()

    def agent_events_processed(id):
        connection = EventData.mon_con()
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE agentevents SET processed=1 WHERE id<=" + str(id)
                cursor.execute(sql)
                connection.commit()
        finally: connection.close()

    def agent_filter_select(id):
        connection = EventData.mon_con()
        try:
            with connection.cursor() as cursor:
                sql = """select t1.notify_email, t1.notify_name, t2.id, t2.timestamp, t2.name, t2.monitor, t2.message, t2.severity, t2.status FROM notifyrule as t1 
                      INNER JOIN agentevents as t2 on 
                      t2.name LIKE t1.agent_name AND t2.monitor LIKE t1.agent_monitor 
                      AND t2.status LIKE t1.agent_status AND t2.severity LIKE t1.agent_severity AND t2.processed=0 AND T2.id<=""" + str(id) + " AND t1.notify_enabled=1"
                cursor.execute(sql)
                result = cursor.fetchall()
                agent_events_processed(id)
                return result
        finally: connection.close()

    def agent_avail_select(timestamp):
        connection = EventData.mon_con()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT name FROM agentsystem WHERE timestamp<" + timestamp
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        finally: connection.close()

    def agent_avail_event_open(timestamp, name, message, severity):
        connection = EventData.mon_con()
        try:
            with connection.cursor() as cursor:
                sql = r"""INSERT INTO agentevents 
                (timestamp, name, monitor, message, status, severity, processed) 
                SELECT """ + str(timestamp) + """, '""" + name + """', 'perf.system.availability.seconds', '""" + message + """', 1, """ + str(severity) + """, 0 FROM DUAL
                WHERE NOT EXISTS (SELECT name FROM agentevents WHERE name='""" + name + """' AND monitor='perf.system.availability.seconds' AND status=1)"""
                cursor.execute(sql)
                connection.commit()
        finally: connection.close()        

    def agent_avail_select_event_open(timestamp):
        connection = EventData.mon_con()
        try:
            with connection.cursor() as cursor:
                sql = r"""SELECT DISTINCT t1.name FROM agentevents as t1 
                INNER JOIN agentdata as t2 on t1.name = t2.name
                WHERE t1.monitor='perf.system.availability.seconds' AND t1.status=1 AND t2.timestamp >=""" + str(timestamp)
                cursor.execute(sql)
                result = cursor.fetchall()
                if not result is None:
                    for i in result:
                        name = i['name']
                        #print(name)
                        sql = r"UPDATE agentevents SET status=0 WHERE name='" + name + "'"
                        cursor.execute(sql)
                        connection.commit()
        finally: connection.close()

class EventAvailable():
    def check_available():
        try:
            check_time = str(time.time() - EventSettings.availability_check).split('.')[0]
            cur_time = str(time.time()).split('.')[0]
            hosts = EventData.agent_avail_select(check_time)
            for i in hosts:
                name = i["name"]
                message = "Agent not responding for " + str(int(round(EventSettings.availability_check / 60,0)))  + " minutes"
                EventData.agent_avail_event_open(cur_time, name, message, str(EventSettings.availability_severity))
                #print(message)
        except: pass

    def check_open():
        try:
            check_time = str(time.time() - EventSettings.availability_check).split('.')[0]
            EventData.agent_avail_select_event_open(check_time)
        except: pass

class ServerEvent():
    def process_events():
        try:
            id = EventData.agent_select_id()
            output = EventData.agent_filter_select(id)
            for i in output:
                notify_email = i["notify_email"]
                notify_name = i["notify_name"]
                name = i["name"]
                monitor = i["monitor"]
                message = i["message"]
                severity = ""
                if i["severity"] == "1": severity = "critical"
                if i["severity"] == "2": severity = "major"
                if i["severity"] == "3": severity = "warning"
                if i["severity"] == "4": severity = "info"
                status = ""
                if i["status"] == "0": status = "closed"
                else: status = "open"
                timestamp = int(i["timestamp"])
                date = datetime.datetime.fromtimestamp(timestamp)
                email_subject = name + ":" + monitor + ":" + severity + ":" + status 
                email_message = """<div style="font-family:Arial, Helvetica, sans-serif;font-size: 11pt"><b>message:</b> """ + message + "<br /><b>name:</b> " + name + "<br /><b>monitor:</b> " + monitor + "<br /><b>severity:</b> " + severity + "<br /><b>status:</b> " + status + "<br /><b>time opened:</b> " + str(date) + "<br /><b>policy:</b> " + notify_name + "</div>"

                if EventSettings.mailactive == 1:
                    msg = EmailMessage()
                    msg["Subject"] = email_subject
                    msg["From"] = EventSettings.mailadmin
                    msg["To"] = notify_email
                    msg.set_content(email_message, subtype='html')
                    s = smtplib.SMTP(EventSettings.mailserver)
                    s.send_message(msg)
                    s.quit()

                #print(str(time.time()).split('.')[0] + ":" + notify_email + ":" + notify_name + ":" + name + ":" + monitor + ":" + message + ":" + severity + ":" +status + ":" + str(date) + "\n")
                f = open(EventSettings.application_path + "output.txt","a")
                f.write(str(time.time()).split('.')[0] + ":" + notify_email + ":" + notify_name + ":" + name + ":" + monitor + ":" + message + ":" + severity + ":" +status + ":" + str(date) + "\n")
                f.close()
        except: pass

#EventConfig.load_config()
#EventAvailable.check_available()
#EventAvailable.check_open()
#ServerEvent.process_events()
