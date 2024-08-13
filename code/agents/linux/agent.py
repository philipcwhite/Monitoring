# Copyright (C) 2018-2021 Phil White - All Rights Reserved
# 
# You may use, distribute and modify this code under the terms of the Apache 2 license. You should have received a 
# copy of the Apache 2 license with this file. If not, please visit:  https://github.com/philipcwhite/monitoring

import configparser, datetime, json, os, platform, socket, sqlite3, ssl, subprocess, time

session = {}
session['running'] = True
session['path'] = './' #'/opt/monitoring/agent/'
session['passphrase'] = 'secure_monitoring'
session['server'] = '127.0.0.1'
session['port'] = 8888

class Data():
    def __init__(self):
        self.con = sqlite3.connect(session['path'] + 'agent_sqlite.db', isolation_level=None)
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
        sql = "DELETE FROM AgentData WHERE time<?;"
        self.cursor.execute(sql, [agent_time])
        sql = "DELETE FROM AgentEvents WHERE status=0 AND sent=1;"
        self.cursor.execute(sql)
        self.con.commit()

    def delete_thresholds(self):
        sql = "DELETE FROM AgentThresholds;"
        self.cursor.execute(sql)
        self.con.commit()

    def insert_data(self, monitor, value):
        sql = "INSERT INTO AgentData(time, name, monitor, value, sent) VALUES (?,?,?,?,?);"
        self.cursor.execute(sql,(session['time'], session['name'], monitor, value, 0))
        self.con.commit()

    def insert_event(self, monitor, message, severity):
        sql = "UPDATE AgentEvents SET time=?, message=?, severity=?, sent=0 WHERE monitor=? AND ?> (SELECT MAX(severity) FROM AgentEvents WHERE monitor=? AND status=1);"
        self.cursor.execute(sql, (session['time'], message, severity, monitor, severity, monitor))
        sql = "INSERT INTO AgentEvents(time, name, monitor, message, status, severity, sent) SELECT ?,?,?,?,1,?,0 WHERE NOT EXISTS(SELECT 1 FROM AgentEvents WHERE monitor=? AND status=1);"
        self.cursor.execute(sql, (session['time'], session['name'], monitor, message, severity, monitor))
        self.con.commit()

    def insert_system(self, ipaddress, os, build, architecture, domain, processors, memory):
        sql = "UPDATE AgentSystem SET time=?, name=?, ipaddress=?, platform=?, architecture=?, domain=?, processors=?, memory=? WHERE name=?;" 
        self.cursor.execute(sql, (session['time'], session['name'], ipaddress, os, architecture, domain, processors, memory, session['name']))
        sql = "INSERT INTO AgentSystem(time, name, ipaddress, platform, build, architecture, domain, processors, memory) SELECT ?,?,?,?,?,?,?,?,? WHERE NOT EXISTS(SELECT 1 FROM AgentSystem WHERE name=?);"
        self.cursor.execute(sql, (session['time'], session['name'], ipaddress, os, build, architecture, domain, processors, memory, session['name']))
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
        sql = "SELECT value FROM AgentData WHERE monitor=? AND time > ?;"
        self.cursor.execute(sql, (monitor, str(time)))
        rows = self.cursor.fetchall()
        return rows

    def select_event(self, monitor):
        sql = "SELECT monitor FROM AgentEvents WHERE monitor=? AND status=1;" 
        self.cursor.execute(sql, [monitor])
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
        sql = "UPDATE AgentData SET sent=1 WHERE sent=0; UPDATE AgentEvents SET sent=1 WHERE sent=0;"
        self.cursor.executescript(sql)
        self.con.commit()

    def update_event(self, monitor, severity):
        sql =  "UPDATE AgentEvents SET status=0, sent=0 WHERE monitor=? AND severity=?;"
        self.cursor.execute(sql, (monitor, str(severity)))
        self.con.commit()

# Initialize Data Class
SQL = Data()

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
        SQL.insert_system(ipaddress, osplatform, build, architecture, domain, processors, memory)

    def perf_filesystem():
        output = subprocess.run('df -x tmpfs -x devtmpfs | tail -n +2', shell=True, capture_output=True, text=True).stdout.split('\n')
        for i in output:
            if '%' in i:
                fs = i.split()
                fs = i.split()
                fs_name = f'perf.filesystem.{fs[0]}.percent.used'
                fs_name = fs_name.replace('/','.').replace('..','.')
                fs_used = str(fs[4].replace('%',''))
                SQL.insert_data(fs_name, fs_used)

    def perf_memory():
        output = subprocess.run('free -m', shell=True, capture_output=True, text=True).stdout.split('\n')[1].split()[1:]
        memory_used = round((((float(output[0])-float(output[5]))/float(output[0])))*100,0)
        SQL.insert_data('perf.memory.percent.used', str(memory_used))

    def perf_network():
        br = bs = br_min = bs_min= 0
        output = subprocess.run('cat /proc/net/dev | tail -n +3', shell=True, capture_output=True, text=True).stdout.split('\n')
        for i in output:
            if ':' in i and not 'lo:' in i:
                net = i.split()
                br += int(net[1])
                bs += int(net[9])
        if 'bytes_received' in session:
            br_min = round((br - session['bytes_received'])/60, 0)
            bs_min = round((bs - session['bytes_sent'])/60, 0)
        session['bytes_received'] = br
        session['bytes_sent'] = bs
        SQL.insert_data('perf.network.bytes.received', str(br_min))
        SQL.insert_data('perf.network.bytes.sent', str(bs_min))

    def perf_pagefile():
        output = subprocess.run('free -m', shell=True, capture_output=True, text=True).stdout.split('\n')[2].split()[1:]
        swap_used = round((float(output[1])/float(output[0]))*100,0)
        SQL.insert_data('perf.pagefile.percent.used', str(swap_used))

    def perf_processes():
        if session['processes']:
            for i in session['processes']:
                output = subprocess.run('ps -C ' + i + ' >/dev/null && echo 1 || echo 0', shell=True, capture_output=True, text=True).stdout.replace('\n','')
                sname = 'perf.process.' + i.replace(' ','').lower() + '.state'
                SQL.insert_data(sname, str(output))
    
    def perf_processor():
        output = subprocess.run('top -b -n2 -p1 -d.1| grep -oP "(?<=ni, ).[0-9]*.[0-9]" | tail -1', shell=True, capture_output=True, text=True).stdout
        cpu_avg = round(100 - float(output.replace('\n','')),0)
        SQL.insert_data('perf.processor.percent.used', str(cpu_avg))
    
    def perf_uptime():
        output = subprocess.run('cat /proc/uptime', shell=True, capture_output=True, text=True).stdout.split()[0]
        uptime = int(round(float(output),0))
        SQL.insert_data('perf.system.uptime.seconds', str(uptime))
   
class AgentProcess():
    def initialize_agent():
        try:
            SQL.create_tables()
            SQL.delete_thresholds()
            parser = configparser.ConfigParser()
            parser.read(session['path'] + 'settings.ini')
            config = dict(parser.items('configuration'))
            thresholds = list(dict(parser.items('thresholds')).values())
            for i in thresholds: 
                thresh = i.split(',')
                SQL.insert_thresholds(thresh[0], thresh[1], thresh[2], thresh[3], thresh[4])
            session['name'] = socket.gethostname().lower()
            session['server'] = config['server']
            session['passphrase'] = config['passphrase']
            session['port'] = int(config['port'])
            session['secure'] = eval(config['secure'])
            session['log'] = eval(config['log'])
            session['processes'] = list(dict(parser.items('processes')).values())
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
        check_monitor = SQL.select_event(monitor)
        if not check_monitor is None: check_monitor=check_monitor[0]
        if check_monitor is None and status == 1: SQL.insert_event(monitor, message, severity)
        elif check_monitor == monitor and status == 0: SQL.update_event(monitor, severity)
        else: pass
        
    def event_process():
        agent_time_int = int(session['time'])
        agent_thresholds = SQL.select_thresholds()
        status = 0
        for i in agent_thresholds:
            monitor = i[0]
            severity = i[1]
            threshold = int(i[2])
            compare = i[3]
            duration = i[4]
            time_window = agent_time_int - duration
            agent_data = SQL.select_data_events(time_window, monitor)
            a_val = b_val = 0
            for i in agent_data:
                value = i[0]
                if eval(str(value) + compare + str(threshold)) is True:
                    a_val += 1
                    b_val += 1
                else: b_val += 1
            if a_val == b_val and b_val != 0: status = 1                
            AgentProcess.event_create(monitor, severity, threshold, compare, duration, status)

    def create_packet():
        system = SQL.select_system()
        events = SQL.select_events()
        data = SQL.select_data()
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
                  "passphrase": session['passphrase'],
                  "data": agent_data,
                  "events": agent_events}
        packet = json.dumps(packet)
        return packet

    def send_data(message):
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            if session['secure'] == 1:
                context = ssl.create_default_context()
                context.options |= ssl.PROTOCOL_TLSv1_2
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                conn = context.wrap_socket(sock, server_hostname = session['server'])
                conn.connect((session['server'], session['port']))
                messagebytes=str(message).encode()
                conn.sendall(messagebytes)
                data = conn.recv(1024).decode()
                if data == 'Received': SQL.update_close_data_events()
                conn.close()
            else:
                sock.connect((session['server'], session['port']))
                messagebytes=str(message).encode()
                sock.sendall(messagebytes)
                data = sock.recv(1024).decode()
                if data == 'Received': SQL.update_close_data_events()
                sock.close()
        except: pass

    def run_process():
        while session['running'] == True:
            a = datetime.datetime.now().second
            if a == 0:
                session['time'] = str(time.time()).split('.')[0]
                AgentProcess.data_process()
                AgentProcess.event_process()
                AgentProcess.send_data(AgentProcess.create_packet())
                SQL.delete_data_events()
            time.sleep(1)

AgentProcess.initialize_agent()
AgentProcess.run_process()
