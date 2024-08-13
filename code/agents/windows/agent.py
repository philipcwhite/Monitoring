# Copyright (C) 2018-2019 Phil White - All Rights Reserved
# 
# You may use, distribute and modify this code under the terms of the Apache 2 license. You should have received a 
# copy of the Apache 2 license with this file. If not, please visit:  https://github.com/philipcwhite/monitoring

import configparser, datetime, json, os, platform, re, socket, sqlite3, ssl, subprocess, time

class AgentSettings:
    log = False
    name = None
    passphrase = 'secure_monitoring'
    path = 'C:\\Progra~1\\monitoring\\agent\\'
    port = 8888
    running = True
    secure = False
    server = '127.0.0.1'
    services = []
    time = None
    
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

class AgentWindows():
    def conf_system():
        memory = subprocess.run('wmic path Win32_ComputerSystem get TotalPhysicalMemory /value', shell=True, capture_output=True, text=True).stdout
        memory = re.search(r'(?m)(?<=\bTotalPhysicalMemory=).*$', memory).group()
        memory = round(int(memory)  / 1048576, 0)
        osplatform = platform.system()
        architecture = platform.architecture()[0]
        build = platform.win32_ver()[1]
        ipaddress= socket.gethostbyname(socket.gethostname())
        processors = str(os.cpu_count())
        domain = socket.getfqdn()
        if '.' in domain: domain = domain.split('.', 1)[1]
        else: domain = 'Stand Alone'
        ASQL.insert_system(ipaddress, osplatform, build, architecture, domain, processors, memory)

    def perf_filesystem():
        result = subprocess.run('''wmic path Win32_PerfFormattedData_PerfDisk_LogicalDisk WHERE "Name LIKE '%:'" get Name,PercentFreeSpace,PercentIdleTime /format:csv''', shell=True, capture_output=True, text=True).stdout
        result_list = result.split('\n')
        for i in result_list:
            if not 'PercentFreeSpace' in i and ',' in i:
                ld_list = i.split(',')
                ld_name = ld_list[1].replace(':','').lower()
                ASQL.insert_data('perf.filesystem.' + ld_name + '.percent.used', str(100 - float(ld_list[2])))
                ASQL.insert_data('perf.filesystem.' + ld_name + '.percent.active', str(100 - float(ld_list[3])))

    def perf_memory():
        result = subprocess.run('wmic path Win32_OperatingSystem get FreePhysicalMemory,TotalVisibleMemorySize /value', shell=True, capture_output=True, text=True).stdout 
        FreeMem = int(re.search(r'(?m)(?<=\bFreePhysicalMemory=).*$', result).group())
        TotalMem = int(re.search(r'(?m)(?<=\bTotalVisibleMemorySize=).*$', result).group())
        PercentMem = ((TotalMem-FreeMem)/TotalMem)*100
        PercentMem = round(PercentMem, 0)
        ASQL.insert_data('perf.memory.percent.used', str(PercentMem))

    def perf_network():
        nw_br = 0
        nw_bs = 0
        result = subprocess.run('wmic path Win32_PerfFormattedData_Tcpip_NetworkInterface get BytesReceivedPersec,BytesSentPersec /format:csv', shell=True, capture_output=True, text=True).stdout
        result_list = result.split('\n')
        for i in result_list:
            if not 'BytesReceivedPersec' in i and ',' in i:
                nw_list = i.split(",")
                nw_br += int(nw_list[1])
                nw_bs += int(nw_list[2])
        ASQL.insert_data('perf.network.bytes.received', str(nw_br))
        ASQL.insert_data('perf.network.bytes.sent', str(nw_bs))

    def perf_pagefile():
        result = subprocess.run('wmic path Win32_PerfFormattedData_PerfOS_PagingFile where name="_Total" get PercentUsage /value', shell=True, capture_output=True, text=True).stdout
        result = str(re.search(r'(?m)(?<=\bPercentUsage=).*$', result).group())
        ASQL.insert_data('perf.pagefile.percent.used', result)
    
    def perf_processor():
        result = subprocess.run('wmic path Win32_PerfFormattedData_PerfOS_Processor where name="_Total" get PercentProcessorTime /value', shell=True, capture_output=True, text=True).stdout
        result = str(re.search(r'(?m)(?<=\bPercentProcessorTime=).*$', result).group())
        ASQL.insert_data('perf.processor.percent.used', result)
    
    def perf_uptime():
        result = subprocess.run('wmic path Win32_PerfFormattedData_PerfOS_System get SystemUptime /value', shell=True, capture_output=True, text=True).stdout
        result = str(re.search(r'(?m)(?<=\bSystemUpTime=).*$', result).group())
        ASQL.insert_data('perf.system.uptime.seconds', result)
    
    def perf_services():
        if AgentSettings.services:
            for service in AgentSettings.services:
                result = subprocess.run('wmic path Win32_Service where name="' + service + '" get State /value', shell=True, capture_output=True, text=True).stdout
                result = str(re.search(r'(?m)(?<=\bState=).*$', result).group())
                sname = 'perf.service.' + service.replace(' ','').lower() + '.state'
                if result == 'Running': result = 1
                else: result = 0
                ASQL.insert_data(sname, str(result))

class AgentProcess():
    def initialize_agent():
        try:
            AgentSettings.name = socket.gethostname().lower()
            ASQL.create_tables()
            ASQL.delete_thresholds()
            parser = configparser.ConfigParser()
            parser.read(AgentSettings.path + 'settings.ini')
            config = dict(parser.items('configuration'))
            services = list(dict(parser.items('services')).values())
            thresholds = list(dict(parser.items('thresholds')).values())
            AgentSettings.log = eval(config['log'])
            AgentSettings.passphrase = config['passphrase']
            AgentSettings.port = int(config['port'])
            AgentSettings.server = config['server']
            AgentSettings.secure = eval(config['secure'])
            AgentSettings.services = services
            for i in thresholds: 
                thresh = i.split(',')
                ASQL.insert_thresholds(thresh[0], thresh[1], thresh[2], thresh[3], thresh[4])
        except: pass

    def data_process():
        try:
            AgentWindows.conf_system()
            AgentWindows.perf_filesystem()
            AgentWindows.perf_memory()
            AgentWindows.perf_network()
            AgentWindows.perf_pagefile()
            AgentWindows.perf_processor()
            AgentWindows.perf_uptime()
            AgentWindows.perf_services()
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
        #print(packet)
        return packet
        
    def send_data(message):
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            if AgentSettings.secure == True:
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
                AgentProcess.create_packet()
                AgentProcess.send_data(AgentProcess.create_packet())
                ASQL.delete_data_events()
            time.sleep(1)
