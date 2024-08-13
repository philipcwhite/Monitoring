import datetime, configparser, os, smtplib, time, sqlite3
from email.message import EmailMessage

class EventSettings:
    app_path = './'
    availability_check = 300
    availability_severity = 1
    agent_retention = 2592000
    data_retention = 2592000
    event_retention = 2592000
    mailactive = 0
    mailadmin = 'monitoring@monitoring'
    mailserver = 'localhost'
    running = True

class EventConfig:
    def load_config():
        try:
            EventSettings.running = True 
            parser = configparser.ConfigParser()
            parser.read(EventSettings.app_path + 'settings.ini')
            events = dict(parser.items('events'))
            mail = dict(parser.items('mail'))
            retention = dict(parser.items('retention'))
            EventSettings.agent_retention = int(retention['agent'])
            EventSettings.data_retention = int(retention['data'])
            EventSettings.event_retention = int(retention['event'])
            EventSettings.mailactive = int(mail['active'])
            EventSettings.mailserver = mail['server']
            EventSettings.mailadmin = mail['admin']
            EventSettings.availability_check = int(events['availability_check'])
            EventSettings.availability_severity = int(events['availability_severity'])
        except: pass

class EventData:
    def __init__(self):
        self.con = sqlite3.connect('/opt/monitoring/server/database/flask.db')
        self.cursor = self.con.cursor()
    
    def __del__(self):
        self.con.close()

    def agent_select_id(self):
        sql = 'SELECT id from agentevents ORDER BY id DESC LIMIT 1' 
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        result = str(result[0])
        return result
        
    def agent_events_processed(self, id):
        sql = 'UPDATE agentevents SET processed=1 WHERE id<=?'
        self.cursor.execute(sql, str(id))
        self.con.commit()

    def agent_filter_select(self, id):
        sql = '''select t1.email, t1.name, t2.id, t2.timestamp, t2.name, t2.monitor, t2.message, t2.severity, t2.status FROM notifyrule as t1 
                 INNER JOIN agentevents as t2 on 
                 t2.name LIKE t1.agent AND t2.monitor LIKE t1.monitor 
                 AND t2.status LIKE t1.status AND t2.severity LIKE t1.severity AND t2.processed=0 AND T2.id<=? AND t1.enabled=1'''
        self.cursor.execute(sql, (str(id),))
        result = self.cursor.fetchall()
        self.agent_events_processed(id)
        return result
        
    def agent_avail_select(self, timestamp):
        sql = 'SELECT name FROM agentsystem WHERE timestamp < ?' 
        self.cursor.execute(sql, (str(timestamp),))
        result = self.cursor.fetchall()
        return result
           
    def agent_avail_event_open(self, timestamp, name, message, severity):
        sql = """INSERT INTO agentevents (timestamp, name, monitor, message, status, severity, processed) 
                SELECT ?, ?, 'perf.system.availability.seconds', ?, 1, ?, 0 NOT IN (SELECT name FROM agentevents WHERE name=? AND monitor='perf.system.availability.seconds' AND status=1)"""
        self.cursor.execute(sql, (str(timestamp), name, message, str(severity), name))
        self.con.commit()

    def agent_avail_select_event_open(self, timestamp):
        sql = """SELECT DISTINCT t1.name FROM agentevents as t1 
              INNER JOIN agentdata as t2 on t1.name = t2.name
              WHERE t1.monitor='perf.system.availability.seconds' AND t1.status=1 AND t2.timestamp >=?""" 
        self.cursor.execute(sql, (str(timestamp),))
        result = self.cursor.fetchall()
        if not result is None:
            for i in result:
                name = i['name']
                sql = "UPDATE agentevents SET status=0 WHERE name=?"
                self.cursor.execute(sql, name)
                self.con.commit()
        
    def remove_agents(self):
        sql = 'DELETE FROM agentsystem WHERE timestamp < ' + str(time.time() - EventSettings.agent_retention) 
        self.cursor.execute(sql)
        self.con.commit()
        
    def remove_events(self):
        sql = 'DELETE FROM agentevents WHERE timestamp < ' + str(time.time() - EventSettings.event_retention) 
        self.cursor.execute(sql)
        self.con.commit()
        
    def remove_data(self):
        sql = 'DELETE FROM agentdata WHERE timestamp < ' + str(time.time() - EventSettings.data_retention) 
        self.cursor.execute(sql)
        self.con.commit()
        
ED = EventData()

class EventAvailable:
    def check_available():
        '''try:
            check_time = str(time.time() - EventSettings.availability_check).split('.')[0]
            cur_time = str(time.time()).split('.')[0]
            hosts = ED.agent_avail_select(str(check_time))
            for i in hosts:
                name = i[0]
                message = 'Agent not responding for ' + str(int(round(EventSettings.availability_check / 60,0)))  + ' minutes'
                ED.agent_avail_event_open(cur_time, name, message, str(EventSettings.availability_severity))
        except: pass'''

        check_time = str(time.time() - EventSettings.availability_check).split('.')[0]
        cur_time = str(time.time()).split('.')[0]
        hosts = ED.agent_avail_select(str(check_time))
        for i in hosts:
            name = i[0]
            message = 'Agent not responding for ' + str(int(round(EventSettings.availability_check / 60,0)))  + ' minutes'
            ED.agent_avail_event_open(cur_time, name, message, str(EventSettings.availability_severity))


    def check_open():
        check_time = str(time.time() - EventSettings.availability_check).split('.')[0]
        ED.agent_avail_select_event_open(check_time)

        '''try:
            check_time = str(time.time() - EventSettings.availability_check).split('.')[0]
            ED.agent_avail_select_event_open(check_time)
        except: pass'''

class ServerEvent:
    def process_events():
        id = ED.agent_select_id()
        output = ED.agent_filter_select(id)
        for i in output:
            notify_email = i[0]
            notify_name = i[1]
            name = i[4]
            monitor = i[5]
            message = i[6]
            severity = ''
            if i[7] == '1': severity = 'critical'
            if i[7] == '2': severity = 'major'
            if i[7] == '3': severity = 'warning'
            if i[7] == '4': severity = 'info'
            status = ''
            if i[8] == '0': status = 'closed'
            else: status = 'open'
            timestamp = int(i[3])
            date = datetime.datetime.fromtimestamp(timestamp)
            email_subject = name + ':' + monitor + ':' + severity + ':' + status 
            email_message = '''<div style='font-family:Arial, Helvetica, sans-serif;font-size: 11pt'><b>message:</b> ''' + message + '<br /><b>name:</b> ' + name + '<br /><b>monitor:</b> ' + monitor + '<br /><b>severity:</b> ' + severity + '<br /><b>status:</b> ' + status + '<br /><b>time opened:</b> ' + str(date) + '<br /><b>policy:</b> ' + notify_name + '</div>'

            if EventSettings.mailactive == 1:
                msg = EmailMessage()
                msg['Subject'] = email_subject
                msg['From'] = EventSettings.mailadmin
                msg['To'] = notify_email
                msg.set_content(email_message, subtype='html')
                s = smtplib.SMTP(EventSettings.mailserver)
                s.send_message(msg)
                s.quit()
            f = open(EventSettings.app_path + 'output.txt','a')
            f.write(str(time.time()).split('.')[0] + ':' + notify_email + ':' + notify_name + ':' + name + ':' + monitor + ':' + message + ':' + severity + ':' +status + ':' + str(date) + '\n')
            f.close()





def start_server():
    EventConfig.load_config()
    while EventSettings.running == True:
        a = datetime.datetime.now().second
        if a == 0:
            EventAvailable.check_available()
            EventAvailable.check_open()
            ServerEvent.process_events()
            ED.remove_agents()
            ED.remove_data()
            ED.remove_events()
        time.sleep(1)

start_server()