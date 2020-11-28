# Copyright (C) 2018-2020 Phil White - All Rights Reserved
# 
# You may use, distribute and modify this code under the terms of the Apache 2 license. You should have received a 
# copy of the Apache 2 license with this file. If not, please visit:  https://github.com/philipcwhite/monitoring

import configparser, datetime, json, os, platform, socket, sqlite3, ssl, subprocess, time

class AgentSettings:
    log = False
    name = None
    passphrase = 'secure_monitoring'
    path = '/opt/monitoring/agent/'
    port = 8888
    running = True
    secure = False
    server = '127.0.0.1'
    processes = []
    time = None
    bytes_received = 0
    bytes_sent = 0

class AgentSQL():
    def __init__(self):
        self.con = sqlite3.connect(AgentSettings.path + 'agent_sqlite.db', isolation_level=None)
        self.cursor = self.con.cursor()

    def __del__(self):
        self.con.close()

    def create_tables(self):
        sql = "CREATE TABLE IF NOT EXISTS AgentData (time integer,name text,monitor text,value integer,sent integer);"
        sql += "CREATE TABLE IF NOT EXISTS AgentEvents (time integer,name text,monitor text,message text,status integer,severity integer, sent integer);"
        sql += "CREATE TABLE IF NOT EXISTS AgentSystem (time integer, name text, ipaddress text, platform text, build text, architecture text, domain text, processors integer, memory integer);"
        sql += "CREATE TABLE IF NOT EXISTS AgentThresholds (monitor text,severity integer,threshold integer, compare text,duration integer);"
        self.cursor.executescript(sql)
        self.con.commit()

    def delete_data_events(self):
        agent_time = str(time.time()-604800).split('.')[0]
        sql = "DELETE FROM AgentData WHERE time<" + agent_time + ';'
        sql += "DELETE FROM AgentEvents WHERE status=0 AND sent=1;"
        self.cursor.executescript(sql)
        self.con.commit()

    def delete_thresholds(self):
        sql = "DELETE FROM AgentThresholds;"
        self.cursor.execute(sql)
        self.con.commit()

    def insert_data(self, monitor, value):
        sql = "INSERT INTO AgentData(time, name, monitor, value, sent) VALUES (?,?,?,?,?);"
        self.cursor.execute(sql,(AgentSettings.time, AgentSettings.name, monitor, value, 0))
        self.con.commit()

    def insert_event(self, monitor, message, severity):
        sql_update = "UPDATE AgentEvents SET time=?, message=?, severity=?, sent=0 WHERE monitor=? AND ?> (SELECT MAX(severity) FROM AgentEvents WHERE monitor=? AND status=1);"
        self.cursor.execute(sql_update, (AgentSettings.time, message, severity, monitor, severity, monitor))
        sql_insert = "INSERT INTO AgentEvents(time, name, monitor, message, status, severity, sent) "
        sql_insert += "SELECT ?,?,?,?,1,?,0 WHERE NOT EXISTS(SELECT 1 FROM AgentEvents WHERE monitor=? AND status=1);"
        self.cursor.execute(sql_insert, (AgentSettings.time, AgentSettings.name, monitor, message, severity, monitor))
        self.con.commit()

    def insert_system(self, ipaddress, os, build, architecture, domain, processors, memory):
        sql_update = "UPDATE AgentSystem SET time=?, name=?, ipaddress=?, platform=?, architecture=?, domain=?, processors=?, memory=? WHERE name=?;" 
        self.cursor.execute(sql_update, (AgentSettings.time, AgentSettings.name, ipaddress, os, architecture, domain, processors, memory, AgentSettings.name))
        sql_insert = "INSERT INTO AgentSystem(time, name, ipaddress, platform, build, architecture, domain, processors, memory) "
        sql_insert += "SELECT ?,?,?,?,?,?,?,?,? WHERE NOT EXISTS(SELECT 1 FROM AgentSystem WHERE name=?);"
        self.cursor.execute(sql_insert, (AgentSettings.time, AgentSettings.name, ipaddress, os, build, architecture, domain, processors, memory, AgentSettings.name))
        self.con.commit()

    def insert_thresholds(self, monitor, severity, threshold, compare, duration):
        sql = "INSERT INTO AgentThresholds(monitor, severity, threshold, compare, duration) VALUES(?,?,?,?,?);"
        self.cursor.execute(sql, (monitor, severity, threshold, compare, duration))
        self.con.commit()
        
    def select_data(self):
        sql = "SELECT time, name, monitor, value FROM AgentData WHERE sent=0 AND monitor NOT LIKE '%perf.service%'"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows
    
    def select_data_events(self, time, monitor):
        sql = "SELECT value FROM AgentData WHERE monitor='" + monitor + "' AND time > " + str(time) + ";"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows

    def select_event(self, monitor):
        sql = "SELECT monitor FROM AgentEvents WHERE monitor='" + monitor + "' AND status=1;" 
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        return row

    def select_events(self):
        sql = "SELECT time, name, monitor, message, status, severity FROM AgentEvents WHERE sent=0" 
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows

    def select_system(self):
        sql = "SELECT time, name, ipaddress, platform, build, architecture, domain, processors, memory FROM AgentSystem"
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        return row 

    def select_thresholds(self):
        sql = "SELECT monitor, severity, threshold, compare, duration FROM AgentThresholds"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows   
    
    def update_close_data_events(self):
        sql = "UPDATE AgentData SET sent=1 WHERE sent=0;"
        sql += "UPDATE AgentEvents SET sent=1 WHERE sent=0;"
        self.cursor.executescript(sql)
        self.con.commit()

    def update_event(self, monitor, severity):
        sql =  "UPDATE AgentEvents SET status=0, sent=0 WHERE monitor='" + monitor + "' AND severity=" + str(severity) + ";"
        self.cursor.execute(sql)
        self.con.commit()

# Initialize AgentSQL Class
ASQL = AgentSQL()

class AgentLinux():
    def conf_system():
        memory = subprocess.run('free -m', shell=True, capture_output=True, text=True).stdout.split('\n')[1].split()[1:]
        memory =  str(memory[0])
        build_name = subprocess.run('cat /etc/os-release|grep -oP "(?<=^NAME=).*"', shell=True, capture_output=True, text=True).stdout.replace('"','').replace('\n','')
        build_version = subprocess.run('cat /etc/os-release|grep -oP "(?<=^VERSION_ID=).*"', shell=True, capture_output=True, text=True).stdout.replace('"','').replace('\n','')
        osplatform = platform.system()
        architecture = platform.architecture()[0]
        build = build_name + ' ' + build_version
        ipaddress= socket.gethostbyname(socket.gethostname())
        processors = str(os.cpu_count())
        domain = socket.getfqdn()
        if '.' in domain: domain = domain.split('.', 1)[1]
        else: domain = 'Stand Alone'
        ASQL.insert_system(ipaddress, osplatform, build, architecture, domain, processors, memory)

    def perf_filesystem():
        output = subprocess.run('df -x tmpfs -x devtmpfs | tail -n +2', shell=True, capture_output=True, text=True).stdout.split('\n')
        for i in output:
            if '%' in i:
                fs = i.split()
                fs = i.split()
                fs_name = 'perf.filesystem.' + fs[0] + '.percent.used'
                fs_name = fs_name.replace('/','.').replace('..','.')
                fs_used = str(fs[4].replace('%',''))
                ASQL.insert_data(fs_name, fs_used)

    def perf_memory():
        output = subprocess.run('free -m', shell=True, capture_output=True, text=True).stdout.split('\n')[1].split()[1:]
        memory_used = round( (((float(output[0])-float(output[5]))/float(output[0])))*100,0)
        ASQL.insert_data('perf.memory.percent.used', str(memory_used))

    def perf_network():
        check_bytes_received = 0
        check_bytes_sent = 0
        bytes_received = 0
        bytes_sent = 0
        output = subprocess.run('cat /proc/net/dev | tail -n +3', shell=True, capture_output=True, text=True).stdout.split('\n')
        for i in output:
            if ':' in i and not 'lo:' in i:
                net = i.split()
                #Receive/Transmit
                check_bytes_received += int(net[1])
                check_bytes_sent += int(net[9])
        if AgentSettings.bytes_received != 0:
            bytes_received = round((check_bytes_received - AgentSettings.bytes_received)/60, 0)
            bytes_sent = round((check_bytes_sent - AgentSettings.bytes_sent)/60, 0)
            ASQL.insert_data('perf.network.bytes.received', str(bytes_received))
            ASQL.insert_data('perf.network.bytes.sent', str(bytes_sent))
            AgentSettings.bytes_received = check_bytes_received
            AgentSettings.bytes_sent = check_bytes_sent
        if AgentSettings.bytes_received == 0:
            AgentSettings.bytes_received = check_bytes_received
            AgentSettings.bytes_sent = check_bytes_sent
            ASQL.insert_data('perf.network.bytes.received', '0')
            ASQL.insert_data('perf.network.bytes.sent', '0')

    def perf_pagefile():
        output = subprocess.run('free -m', shell=True, capture_output=True, text=True).stdout.split('\n')[2].split()[1:]
        swap_used = round((float(output[1])/float(output[0]))*100,0)
        ASQL.insert_data('perf.pagefile.percent.used', str(swap_used))

    def perf_processes():
        if AgentSettings.processes:
            for i in AgentSettings.processes:
                output = subprocess.run('ps -C ' + i + ' >/dev/null && echo 1 || echo 0', shell=True, capture_output=True, text=True).stdout.replace('\n','')
                sname = 'perf.process.' + i.replace(' ','').lower() + '.state'
                ASQL.insert_data(sname, str(output))
    
    def perf_processor():
        output = subprocess.run('top -b -n2 -p1 -d.1| grep -oP "(?<=ni, ).[0-9]*.[0-9]" | tail -1', shell=True, capture_output=True, text=True).stdout
        cpu_avg = round(100 - float(output.replace('\n','')),0)
        ASQL.insert_data('perf.processor.percent.used', str(cpu_avg))
    
    def perf_uptime():
        output = subprocess.run('cat /proc/uptime', shell=True, capture_output=True, text=True).stdout.split()[0]
        uptime = int(round(float(output),0))
        ASQL.insert_data('perf.system.uptime.seconds', str(uptime))
   
class AgentProcess():
    def initialize_agent():
        try:
            AgentSettings.name = socket.gethostname().lower()
            ASQL.create_tables()
            ASQL.delete_thresholds()
            parser = configparser.ConfigParser()
            parser.read(AgentSettings.path + 'settings.ini')
            config = dict(parser.items('configuration'))
            processes = list(dict(parser.items('processes')).values())
            thresholds = list(dict(parser.items('thresholds')).values())
            AgentSettings.server = config['server']
            AgentSettings.passphrase = config['passphrase']
            AgentSettings.port = int(config['port'])
            AgentSettings.secure = eval(config['secure'])
            AgentSettings.log = eval(config['log'])
            AgentSettings.processes = processes
            for i in thresholds: 
                thresh = i.split(',')
                ASQL.insert_thresholds(thresh[0], thresh[1], thresh[2], thresh[3], thresh[4])
        except: pass

    def data_process():
        try:
            AgentLinux.conf_system()
            AgentLinux.perf_filesystem()
            AgentLinux.perf_memory()
            AgentLinux.perf_network()
            AgentLinux.perf_pagefile()
            AgentLinux.perf_processor()
            AgentLinux.perf_uptime()
            AgentLinux.perf_processes()
        except: pass
        
    def event_create(monitor, severity, threshold, compare, duration, status):
        message = monitor.replace('perf.', '').replace('.', ' ').capitalize()
        message = message + ' ' + compare + ' ' + str(threshold) + ' for ' + str(round(duration/60)) + ' minutes'
        check_monitor = ASQL.select_event(monitor)
        if not check_monitor is None: check_monitor=check_monitor[0]
        if check_monitor is None and status == 1: ASQL.insert_event(monitor, message, severity)
        elif check_monitor == monitor and status == 0: ASQL.update_event(monitor, severity)
        else: pass
        
    def event_process():
        agent_time_int = int(AgentSettings.time)
        agent_thresholds = ASQL.select_thresholds()
        a_val = 0
        b_val = 0
        for i in agent_thresholds:
            monitor = i[0]
            severity = i[1]
            threshold = int(i[2])
            compare = i[3]
            duration = i[4]
            time_window = agent_time_int - duration
            agent_data = ASQL.select_data_events(time_window, monitor)
            a_val = 0
            b_val = 0
            for i in agent_data:
                value = i[0]
                if compare == '>':
                    if value > threshold:
                        a_val += 1
                        b_val += 1
                    else: b_val += 1
                elif compare == '<':
                    if value < threshold:
                        a_val += 1
                        b_val += 1
                    else: b_val += 1
                elif compare == '=':
                    if value == 0 and threshold == 0:
                        a_val += 1
                        b_val += 1
                    else: b_val += 1
            if a_val == b_val and b_val != 0 :
                AgentProcess.event_create(monitor, severity, threshold, compare, duration, 1)
            else:
                AgentProcess.event_create(monitor, severity, threshold, compare, duration, 0)

    def create_packet():
        system = ASQL.select_system()
        events = ASQL.select_events()
        data = ASQL.select_data()
        agent_data = []
        agent_events = []
        for i in events: agent_events.append({"time":i[0],"monitor":i[2],"message":i[3],"status":i[4],"severity":i[5]})
        for i in data: agent_data.append({"time":i[0],i[2]:i[3]})
        packet = {"time": system[0],
                  "name": system[1],
                  "ip": system[2],
                  "platform": system[3],
                  "build": system[4],
                  "arch": system[5],
                  "domain": system[6],
                  "procs": system[7],
                  "memory": system[8],
                  "passphrase": AgentSettings.passphrase,
                  "data": agent_data,
                  "events": agent_events}
        packet = json.dumps(packet)
        return packet

    def send_data(message):
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            if AgentSettings.secure == 1:
                context = ssl.create_default_context()
                context.options |= ssl.PROTOCOL_TLSv1_2
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                conn = context.wrap_socket(sock, server_hostname = AgentSettings.server)
                conn.connect((AgentSettings.server, AgentSettings.port))
                messagebytes=str(message).encode()
                conn.sendall(messagebytes)
                data = conn.recv(1024).decode()
                if data == 'Received': ASQL.update_close_data_events()
                conn.close()
            else:
                sock.connect((AgentSettings.server, AgentSettings.port))
                messagebytes=str(message).encode()
                sock.sendall(messagebytes)
                data = sock.recv(1024).decode()
                if data == 'Received': ASQL.update_close_data_events()
                sock.close()
        except: pass

    def run_process():
        while AgentSettings.running == True:
            a = datetime.datetime.now().second
            if a == 0:
                AgentSettings.time = str(time.time()).split('.')[0]
                AgentProcess.data_process()
                AgentProcess.event_process()
                AgentProcess.send_data(AgentProcess.create_packet())
                ASQL.delete_data_events()
            time.sleep(1)

AgentProcess.initialize_agent()
AgentProcess.run_process()
