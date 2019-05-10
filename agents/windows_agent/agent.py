# Copyright (C) 2018-2019 Phil White - All Rights Reserved
# 
# You may use, distribute and modify this code under the terms of the Apache 2 license. You should have received a 
# copy of the Apache 2 license with this file. If not, please visit:  https://github.com/philipcwhite/monitoring

import configparser, datetime, os, platform, re, socket, sqlite3, ssl, subprocess, time

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
    def sql_con():
        database = AgentSettings.path + 'agent_sqlite.db'
        con = sqlite3.connect(database, isolation_level=None)
        return con

    def create_tables():
        sql_create_agent_data = "CREATE TABLE IF NOT EXISTS AgentData (time integer,name text,monitor text,value integer,sent integer);"
        sql_create_agent_events = "CREATE TABLE IF NOT EXISTS AgentEvents (time integer,name text,monitor text,message text,status integer,severity integer, sent integer);"
        sql_create_agent_thresholds = "CREATE TABLE IF NOT EXISTS AgentThresholds (monitor text,severity integer,threshold integer, compare text,duration integer);"
        con = AgentSQL.sql_con()
        c = con.cursor()
        c.execute(sql_create_agent_data)
        c.execute(sql_create_agent_events)
        c.execute(sql_create_agent_thresholds)
        con.commit()
        con.close()

    def delete_data_events():
        agent_time = str(time.time()-604800).split('.')[0]
        sql_delete_data = "DELETE FROM AgentData WHERE time<" + agent_time
        sql_delete_events = "DELETE FROM AgentEvents WHERE status=0 AND sent=1"
        con = AgentSQL.sql_con()
        c = con.cursor()
        c.execute(sql_delete_data)
        c.execute(sql_delete_events)
        con.commit()
        con.close()

    def delete_thresholds():
        sql_query = "DELETE FROM AgentThresholds"
        con = AgentSQL.sql_con()
        c = con.cursor()
        c.execute(sql_query)
        con.commit()
        con.close()

    def insert_data(monitor, value):
        sql_query = "INSERT INTO AgentData(time, name, monitor, value, sent) "
        sql_query += "VALUES(" + AgentSettings.time + ",'" + AgentSettings.name + "','" + monitor + "','" + value +  "',0)"
        con = AgentSQL.sql_con()
        c = con.cursor()
        c.execute(sql_query)
        con.commit()
        con.close()

    def insert_event(monitor, message, severity):
        sql_update = "UPDATE AgentEvents SET time=" + str(AgentSettings.time) + ", message='" + message + "', severity=" + str(severity) + ", sent=0 "
        sql_update += "WHERE monitor='" + monitor + "' AND " + str(severity) + "> (SELECT MAX(severity) FROM AgentEvents WHERE monitor='" + monitor + "' AND status=1)"
        sql_insert = "INSERT INTO AgentEvents(time, name, monitor, message, status, severity, sent) "
        sql_insert += "SELECT " + str(AgentSettings.time) + ",'" + AgentSettings.name + "','" + monitor + "','" + message + "',1," + str(severity) + ",0 "
        sql_insert += "WHERE NOT EXISTS(SELECT 1 FROM AgentEvents WHERE monitor='""" + monitor + """' AND status=1)"""
        con = AgentSQL.sql_con()
        c = con.cursor()
        c.execute(sql_update)
        c.execute(sql_insert)
        con.commit()
        con.close()

    def insert_thresholds(monitor, severity, threshold, compare, duration):
        sql_query = "INSERT INTO AgentThresholds(monitor, severity, threshold, compare, duration) "
        sql_query += "VALUES('" + monitor + "'," + severity + "," + threshold + ",'" + compare +  "'," + duration + ")"
        con = AgentSQL.sql_con()
        c = con.cursor()
        c.execute(sql_query)
        con.commit()
        con.close()

    def select_data():
        output = ''
        sql_query = "SELECT time, name, monitor, value FROM AgentData WHERE sent=0 AND monitor NOT LIKE '%perf.service%'"
        con = AgentSQL.sql_con()
        c = con.cursor()
        c.execute(sql_query)
        rows = c.fetchall()
        for time, name, monitor, value in rows:
            output += str(time) + ';' + name + ';' + monitor + ';' + str(value) + '\n'
        con.commit()
        con.close()
        return output
    
    def select_data_events(time, monitor):
        sql_query = "SELECT value FROM AgentData WHERE monitor='" + monitor + "' AND time > " + str(time) 
        con = AgentSQL.sql_con()
        c = con.cursor()
        c.execute(sql_query)
        rows = c.fetchall()
        con.commit()
        con.close()
        return rows

    def select_event(monitor):
        sql_query = "SELECT monitor FROM AgentEvents WHERE monitor='" + monitor + "' AND status=1" 
        con = AgentSQL.sql_con()
        c = con.cursor()
        c.execute(sql_query)
        monitor = c.fetchone()
        con.commit()
        con.close()
        return monitor

    def select_open_events():
        output = ''
        sql_query = "SELECT time, name, monitor, message, status, severity FROM AgentEvents WHERE sent=0" 
        con = AgentSQL.sql_con()
        c = con.cursor()
        c.execute(sql_query)
        rows = c.fetchall()
        for time, name, monitor, message, status, severity in rows:
            output = output + str(time) + ';' + name + ';event;' + monitor + ';' + message + ';' + str(status) + ';' + str(severity) + '\n'
        con.commit()
        con.close()
        return output

    def select_thresholds():
        sql_query = "SELECT monitor, severity, threshold, compare, duration FROM AgentThresholds"
        con = AgentSQL.sql_con()
        c = con.cursor()
        c.execute(sql_query)
        rows = c.fetchall()
        con.commit()
        con.close()
        return rows    
    
    def update_close_data_events():
        sql_update_data = "UPDATE AgentData SET sent=1 WHERE sent=0"
        sql_update_events = "UPDATE AgentEvents SET sent=1 WHERE sent=0"
        con = AgentSQL.sql_con()
        c = con.cursor()
        c.execute(sql_update_data)
        c.execute(sql_update_events)
        con.commit()
        con.close()

    def update_event(monitor, severity):
        sql_query =  "UPDATE AgentEvents SET status=0, sent=0 WHERE monitor='" + monitor + "' AND severity=" + str(severity) 
        con = AgentSQL.sql_con()
        c = con.cursor()
        c.execute(sql_query)
        con.commit()
        con.close()

class AgentWindows():
    def conf_memory_total():
        result = subprocess.run('wmic path Win32_ComputerSystem get TotalPhysicalMemory /value', shell=True, capture_output=True, text=True).stdout
        result = re.search(r'(?m)(?<=\bTotalPhysicalMemory=).*$', result).group()
        result = round(int(result)  / 1048576, 0)
        AgentSQL.insert_data('conf.memory.total', str(result))

    def perf_filesystem():
        result = subprocess.run('''wmic path Win32_PerfFormattedData_PerfDisk_LogicalDisk WHERE "Name LIKE '%:'" get Name,PercentFreeSpace,PercentIdleTime /format:csv''', shell=True, capture_output=True, text=True).stdout
        result_list = result.split('\n')
        for i in result_list:
            if not 'PercentFreeSpace' in i and ',' in i:
                ld_list = i.split(',')
                ld_name = ld_list[1].replace(':','').lower()
                AgentSQL.insert_data('perf.filesystem.' + ld_name + '.percent.used', str(100 - float(ld_list[2])))
                AgentSQL.insert_data('perf.filesystem.' + ld_name + '.percent.active', str(100 - float(ld_list[3])))

    def perf_memory():
        result = subprocess.run('wmic path Win32_OperatingSystem get FreePhysicalMemory,TotalVisibleMemorySize /value', shell=True, capture_output=True, text=True).stdout 
        FreeMem = int(re.search(r'(?m)(?<=\bFreePhysicalMemory=).*$', result).group())
        TotalMem = int(re.search(r'(?m)(?<=\bTotalVisibleMemorySize=).*$', result).group())
        PercentMem = ((TotalMem-FreeMem)/TotalMem)*100
        PercentMem = round(PercentMem, 0)
        AgentSQL.insert_data('perf.memory.percent.used', str(PercentMem))

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
        AgentSQL.insert_data('perf.network.bytes.received', str(nw_br))
        AgentSQL.insert_data('perf.network.bytes.sent', str(nw_bs))

    def perf_pagefile():
        result = subprocess.run('wmic path Win32_PerfFormattedData_PerfOS_PagingFile where name="_Total" get PercentUsage /value', shell=True, capture_output=True, text=True).stdout
        result = str(re.search(r'(?m)(?<=\bPercentUsage=).*$', result).group())
        AgentSQL.insert_data('perf.pagefile.percent.used', result)
    
    def perf_processor():
        result = subprocess.run('wmic path Win32_PerfFormattedData_PerfOS_Processor where name="_Total" get PercentProcessorTime /value', shell=True, capture_output=True, text=True).stdout
        result = str(re.search(r'(?m)(?<=\bPercentProcessorTime=).*$', result).group())
        AgentSQL.insert_data('perf.processor.percent.used', result)
    
    def perf_uptime():
        result = subprocess.run('wmic path Win32_PerfFormattedData_PerfOS_System get SystemUptime /value', shell=True, capture_output=True, text=True).stdout
        result = str(re.search(r'(?m)(?<=\bSystemUpTime=).*$', result).group())
        AgentSQL.insert_data('perf.system.uptime.seconds', result)
    
    def perf_services():
        if AgentSettings.services:
            for service in AgentSettings.services:
                result = subprocess.run('wmic path Win32_Service where name="' + service + '" get State /value', shell=True, capture_output=True, text=True).stdout
                result = str(re.search(r'(?m)(?<=\bState=).*$', result).group())
                sname = 'perf.service.' + service.replace(' ','').lower() + '.state'
                if result == 'Running': result = 1
                else: result = 0
                AgentSQL.insert_data(sname, str(result))

class AgentProcess():
    def initialize_agent():
        try:
            AgentSettings.name = socket.gethostname().lower()
            AgentSQL.create_tables()
            AgentSQL.delete_thresholds()
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
                AgentSQL.insert_thresholds(thresh[0], thresh[1], thresh[2], thresh[3], thresh[4])
        except: pass

    def data_process():
        try:
            AgentSQL.insert_data('conf.os.name', platform.system())
            AgentSQL.insert_data('conf.os.architecture', platform.architecture()[0])
            AgentSQL.insert_data('conf.os.build', platform.win32_ver()[1])
            AgentSQL.insert_data('conf.ipaddress', socket.gethostbyname(socket.gethostname()))
            AgentSQL.insert_data('conf.processors', str(os.cpu_count()))
            domain_name = socket.getfqdn()
            if '.' in domain_name: domain_name = domain_name.split('.', 1)[1]
            else: domain_name = 'Stand Alone'
            AgentSQL.insert_data('conf.domain', domain_name)
        except: pass
        try:
            AgentWindows.conf_memory_total()
            AgentWindows.perf_filesystem()
            AgentWindows.perf_memory()
            AgentWindows.perf_network()
            AgentWindows.perf_pagefile()
            AgentWindows.perf_processor()
            AgentWindows.perf_uptime()
            AgentWindows.perf_services()
        except: pass
        output = AgentSQL.select_data()
        return output
        
    def event_create(monitor, severity, threshold, compare, duration, status):
        message = monitor.replace('perf.', '').replace('.', ' ').capitalize()
        message = message + ' ' + compare + ' ' + str(threshold) + ' for ' + str(round(duration/60)) + ' minutes'
        check_monitor = AgentSQL.select_event(monitor)
        if not check_monitor is None: check_monitor=check_monitor[0]
        if check_monitor is None and status == 1: AgentSQL.insert_event(monitor, message, severity)
        elif check_monitor == monitor and status == 0: AgentSQL.update_event(monitor, severity)
        else: pass
        
    def event_process():
        agent_time_int = int(AgentSettings.time)
        agent_thresholds = AgentSQL.select_thresholds()
        a_val = 0
        b_val = 0
        for i in agent_thresholds:
            monitor = i[0]
            severity = i[1]
            threshold = int(i[2])
            compare = i[3]
            duration = i[4]
            time_window = agent_time_int - duration
            agent_data = AgentSQL.select_data_events(time_window, monitor)
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
        output = AgentSQL.select_open_events()
        if output is None: output = ''
        return output
        
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
                byte=str(message).encode()
                conn.send(byte)
                data = conn.recv(1024).decode()
                if data == 'Received': AgentSQL.update_close_data_events()
                conn.close()
            else:
                sock.connect((AgentSettings.server, AgentSettings.port))
                byte = str(message).encode()
                sock.send(byte)
                data = sock.recv(1024).decode()
                if data == 'Received': AgentSQL.update_close_data_events()
                sock.close()
        except: pass

    def run_process():
        while AgentSettings.running == True:
            a = datetime.datetime.now().second
            if a == 0:
                AgentSettings.time = str(time.time()).split('.')[0]
                header = 'passphrase;' + AgentSettings.passphrase + '\n'
                data_message = AgentProcess.data_process()
                event_message = AgentProcess.event_process()
                message = header + data_message + event_message
                AgentProcess.send_data(message)
                AgentSQL.delete_data_events()
            time.sleep(1)
