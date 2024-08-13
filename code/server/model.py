import sqlite3
import hashlib, datetime, math, socket, time

class Auth:
    def verify(self, user, password):
        D = Data()
        encrypt_password = hashlib.sha224(password.encode()).hexdigest()
        auth = D.user_auth(user, encrypt_password)
        if auth[0] is None: return None
        else: return auth

    def user_password_change(self, user, pass1, pass2):
        D = Data()
        encrypt_password1 = hashlib.sha224(pass1.encode()).hexdigest()
        encrypt_password2 = hashlib.sha224(pass2.encode()).hexdigest()
        authuser = D.user_auth(user, encrypt_password1)
        if not authuser is None:
            D.user_password_change(user, encrypt_password2)
            return True
        return False

    def user_password_change_admin(self, user, pass1, pass2):
        D = Data()
        encrypt_password1 = hashlib.sha224(pass1.encode()).hexdigest()
        encrypt_password2 = hashlib.sha224(pass2.encode()).hexdigest()
        if encrypt_password1 == encrypt_password2:
            D.user_password_change(user, encrypt_password2)
            return True
        return False

    def user_password_set(self, pass1, pass2):
        if pass1 == pass2:
            encrypt_password = hashlib.sha224(pass1.encode()).hexdigest()
            return encrypt_password

    def user_initialize(self):
        #Check if admin user exists. If not create it
        D = Data()
        user = 'admin'
        password = 'password'
        role = 1
        encrypt_password = hashlib.sha224(password.encode()).hexdigest()
        D.user_create_admin(user, encrypt_password, role)

    def user_add(self, user, password, role):
        D = Data()
        encrypt_password = hashlib.sha224(password.encode()).hexdigest()
        D.user_create(user, encrypt_password, role)

class Code:
    def index(self, page):
        index_dict={}
        D = Data()
        uptime_check = 300
        # Block 1
        ok = down = 0
        total = ok + down
        currenttime = time.time()
        agentsystem = D.index_availability()
        for i in agentsystem:
            timestamp = int(i[0])
            if (timestamp + uptime_check) >= currenttime: ok += 1
            else: down += 1
        total = ok + down
        if total == 0: total = 1
        ok_perc = (ok / total) * 100
        down_perc = (down / total) * 100
        total_perc = str(ok_perc) + ' ' + str(down_perc)
        index_dict['avail_ok'] = str(ok)
        index_dict['avail_down'] = str(down) 
        index_dict['avail_total'] = str(total_perc)
        # Block 2
        info = warn = majr = crit = 0
        agentevents = D.event_totals(1)
        for i in agentevents:
            sev = int(i[0])
            sev_tot = int(i[1])
            if sev == 1: crit = sev_tot
            elif sev == 2: majr = sev_tot
            elif sev == 3: warn = sev_tot
            elif sev == 4: info = sev_tot
        total = info + warn + majr + crit
        if total == 0: total = 1
        info_perc = (info / total) * 100
        warn_perc = (warn / total) * 100
        majr_perc = (majr / total) * 100
        crit_perc = (crit / total) * 100
        index_dict['event_info'] = str(info)
        index_dict['event_warn'] = str(warn)
        index_dict['event_majr'] = str(majr)
        index_dict['event_crit'] = str(crit)
        index_dict['event_info_pts'] = str(info_perc) + ' ' + str(100 - info_perc)
        index_dict['event_warn_pts'] = str(warn_perc) + ' ' + str(100 - warn_perc)
        index_dict['event_majr_pts'] = str(majr_perc) + ' ' + str(100 - majr_perc)
        index_dict['event_crit_pts'] = str(crit_perc) + ' ' + str(100 - crit_perc)
        index_dict['event_warn_offset'] = str(100 - info_perc + 25)
        index_dict['event_majr_offset'] = str(100 - info_perc - warn_perc + 25)
        index_dict['event_crit_offset'] = str(100 - info_perc - warn_perc - majr_perc + 25)
        # Block 3
        name = socket.gethostname().lower()
        currenttime = time.time()
        agent_platform = agent_architecture = ''
        agent_timestamp = agent_processors = agent_memory = cpu_perc = mem_perc = 0
        cpu_color = mem_color = online_color = '93C54B'
        agentsystem = D.index_device(name)
        agent_platform = agentsystem[3]
        agent_architecture = agentsystem[5]
        agent_timestamp = agentsystem[0]
        agent_processors = agentsystem[8]
        agent_memory = str(agentsystem[9])[:-3]
        agent_perf = D.device_data_latest(name)
        for i in agent_perf:
            if i[3] == 'perf.processor.percent.used' : cpu_perc = float(i[4])
            if i[3] == 'perf.memory.percent.used' : mem_perc = float(i[4]) #[:-2]
        if cpu_perc >= 90 : cpu_color = 'D9534F'
        if mem_perc >= 90: mem_color = 'D9534F'
        if (agent_timestamp + uptime_check) < currenttime: online_color = 'D9534F'        
        index_dict['agent_name'] = name
        index_dict['agent_processors'] = agent_processors
        index_dict['agent_memory'] = agent_memory
        index_dict['agent_platform'] = agent_platform
        index_dict['agent_architecture'] = agent_architecture
        index_dict['agent_cpu_percent'] = str(cpu_perc)[:-2]
        index_dict['agent_memory_percent'] = str(mem_perc)[:-2]
        index_dict['agent_cpu_color'] = cpu_color
        index_dict['agent_memory_color'] = mem_color
        index_dict['agent_online_color'] = online_color        
        # Block 4
        page_start = (int(page) * 100) - 100
        page_end = page_start + 100
        agentsystem = D.index_device_list(page_start, page_end)
        currenttime = time.time()
        rows = []
        for i in agentsystem:
            row = {}
            row['date'] = str(datetime.datetime.fromtimestamp(int(i[1])))
            color = '93C54B'
            if (int(i[0]) + uptime_check) < currenttime : color = 'D9534F'
            row['color'] = color
            row['name']= name
            row['ipaddress'] = str(i[2])
            row['domain'] = str(i[6]).lower()
            row['platform'] = i[3]
            row['architecture'] = i[5]
            rows.append(row)
        index_dict['host_summary'] = rows
        # Pager
        pager = ''
        agent_count = D.index_device_count()
        page_count = int(math.ceil(int(agent_count[0]) / 100))
        if page_count > 1:
            for i in range(1,page_count + 1):
                if i == page: pager += str(i)
                elif i == 1: pager += f'<a href="/">{str(i)}</a>'
                else: pager += f'<a href="/{str(i)}">{str(i)}</a>&nbsp;'
        index_dict['pager'] = pager
        return index_dict

    def events(self, status):
        events_dict = {}
        D = Data()
        total = info = warn = majr = crit = 0
        agentevents = D.event_totals(status)
        for i in agentevents:
            sev = int(i[0])
            sev_tot = int(i[1])
            if sev == 1: crit = sev_tot
            elif sev == 2: majr = sev_tot
            elif sev == 3: warn = sev_tot
            elif sev == 4: info = sev_tot
        total = info + warn + majr + crit
        status_text = ''
        change_status = abs(int(status) - 1)
        change_status_text = ''
        if change_status == 0:
            status_text = 'Open Events'
            change_status_text = 'Closed Events'
        else:
            status_text = 'Closed Events'
            change_status_text = 'Open Events'
        events_dict['info'] = str(info)
        events_dict['warn'] = str(warn)
        events_dict['majr'] = str(majr)
        events_dict['crit'] = str(crit)
        events_dict['total'] = str(total)
        events_dict['status'] = str(change_status)
        events_dict['status_text'] = status_text
        events_dict['change_text'] = change_status_text
        agentevents = D.events_status(status)
        color = '#CCCCCC'
        change_status = abs(int(status) - 1)
        change_status_text = ""
        if change_status == 0: change_status_text = 'Close Event'
        else: change_status_text = 'Open Event'
        events_dict['change_status'] = change_status
        events_dict['change_status_text'] = change_status_text
        rows = []
        for i in agentevents:
            row = {}
            row['date'] = str(datetime.datetime.fromtimestamp(int(i[1])))
            row['name'] = i[2]
            row['message'] = i[4]
            row['id'] = str(i[0])
            sev_text = ''
            if int(i[5]) == 4:
                row['color'] = '#29ABE0'
                row['severity'] = 'Information'
            elif int(i[5]) == 3:
                row['color']  = '#FFC107'
                row['severity'] = 'Warning'
            elif int(i[5]) == 2:
                row['color']  = '#F47C3C'
                row['severity'] = 'Major'
            elif int(i[5]) == 1:
                row['color']  = '#D9534F'
                row['severity'] = 'Critical'
            rows.append(row)
        events_dict['event_list'] = rows
        return events_dict

    def devices(self):    
        D = Data()
        agentsystem = D.devices_select_all()
        uptime_check = 600
        currenttime = time.time()
        rows = []
        for i in agentsystem:
            row = {}
            if (i[0] + uptime_check) >= currenttime: row['fill'] = '#93C54B'
            else: row['fill'] = '#d9534f'
            row['name'] = i[2]
            row['domain'] = i[7]
            row['ipaddress'] = i[3]
            row['platform'] = i[4]
            rows.append(row)
        return rows

    def device(self, name): 
        device_dict = {}
        D = Data()
        agentsystem = D.device_system(name)
        device_dict['ipaddress'] = agentsystem[3]
        device_dict['domain'] = agentsystem[7].lower()
        device_dict['platform'] = agentsystem[4]
        device_dict['architecture'] = agentsystem[6]
        device_dict['build'] = agentsystem[5]
        device_dict['processors'] = str(agentsystem[8])
        device_dict['memory'] = str(agentsystem[9])[:-3]
        agent_query = D.device_data_latest(name)
        cpu_perc = mem_perc = pagefile_perc = uptime_days = net_br = net_bs = 0
        fs_list = []
        for i in agent_query:
            if i[3] == 'perf.processor.percent.used': device_dict['cpu_perc'] = str(round(float(i[4]), 0))
            if i[3] == 'perf.memory.percent.used': device_dict['mem_perc'] = str(round(float(i[4]), 0))
            if i[3] == 'perf.pagefile.percent.used': device_dict['pagefile_perc'] = str(round(float(i[4]), 0))
            if i[3] == 'perf.system.uptime.seconds': device_dict['uptime_days'] = str(round(float(i[4]) / 86400, 0))
            if i[3] == 'perf.network.bytes.received': device_dict['net_br'] = str(round(float(i[4]), 0))
            if i[3] == 'perf.network.bytes.sent': device_dict['net_bs'] = str(round(float(i[4]), 0))
            if 'filesystem' in i[3] and 'percent.used' in i[3]:
                fs_name = i[3].replace('perf.filesystem.','').replace('.percent.used','')
                fs = (fs_name, str(i[4]))
                fs_list.append(fs)
        return device_dict, fs_list

    def device_graph(self, name, monitor):
        D = Data()
        device_data = D.device_graph(name, monitor)
        data_list = []
        max_value = 0
        graph_time = datetime.datetime.now() - datetime.timedelta(minutes=60)
        for i in range(61):
            data_point = [graph_time.strftime('%H:%M'), 0]
            data_list.append(data_point)
            graph_time = graph_time + datetime.timedelta(minutes=1)
        for i in device_data:
            if float(i[4]) > max_value:max_value = float(i[4])          
        for i in device_data:
            device_value = float(i[4])
            time_short = datetime.datetime.fromtimestamp(int(i[1])).strftime('%H:%M')
            for i in data_list:
                if i[0] == time_short:
                    if device_value == 0: i[1] = 0
                    else: i[1] = (device_value / max_value)*100
        device_polyline = ''
        device_polyline_data = ''
        device_time = ''
        xvalue = 55
        time_x = 0
        for i in data_list:
            dvalue = str(round(110 - i[1]))
            device_polyline_data += str(xvalue) + ',' + dvalue + ' '
            time_x += 1
            if time_x == 1:
                device_time += f'<text x="{str(xvalue)}" y="130" fill="#8E8C84" text-anchor="middle">{str(i[0])}</text>'
            if time_x == 5:
                time_x = 0            
            xvalue += 14 
        device_polyline = f'<polyline points="{device_polyline_data}" style="fill:none;stroke:#29ABE0;stroke-width:1" />'                
        html =  '<svg xmlns="http://www.w3.org/2000/svg" style="color:#8E8C84;" height=150 width=990>'
        html += '<rect x=52 y=10 width=855 height=1 fill=#ddd />'
        html += '<rect x=55 y=35 width=855 height=1 fill=#ddd />'
        html += '<rect x=52 y=60 width=855 height=1 fill=#ddd />'
        html += '<rect x=55 y=85 width=855 height=1 fill=#ddd />'
        html += '<rect x=52 y=110 width=855 height=1 fill=#ddd />'
        html += '<rect x=55 y=10 width=1 height=100 fill=#ddd />'
        html += f'<text x="47" y="15" fill="#8E8C84" text-anchor="end">{str(int(max_value))}</text>'
        html += f'<text x="47" y="65" fill="#8E8C84" text-anchor="end">{str(int(max_value / 2))}</text>'
        html += '<text x="47" y="115" fill="#8E8C84" text-anchor="end">0</text>'
        html += f'{device_polyline}{device_time}</svg>' 
        return html

    def report(self, name, ext):
        D = Data()
        cr = ''
        if ext == 'html': cr = '<br />'
        elif ext == 'csv': cr = '\r\n'
        if name == 'devices':
            devices = D.device_all()
            output = 'Last Reported,Name,IP Address,Platform,Build Number,Architecture,Domain,Processors,Memory' + cr
            for i in devices:
                last_reported = str(datetime.datetime.fromtimestamp(int(i[0])))
                output += last_reported + ',' + str(i[1]) + ',' + str(i[2]) + ',' + str(i[3]) + ',' + str(i[4]) + ',' + str(i[5])
                output +=  ',' + str(i[6]) + ',' + str(i[7]) + ',' + str(i[8]) + cr
        if name == 'events':
            events = D.events(1)
            output = 'Date, Name, Monitor, Message, Severity' + cr
            for i in events:
                last_reported = str(datetime.datetime.fromtimestamp(int(i[0])))
                output += last_reported + ',' + str(i[1]) + ',' + str(i[2]) + ',' + str(i[3]) + ',' + str(i[4]) + cr
        return output

class Data:
    def __init__(self):
        self.con = sqlite3.connect('database/flask.db')
        self.cursor = self.con.cursor()

    def __del__(self):
        self.con.close()

    def create_tables(self):
        agentdata = 'CREATE TABLE IF NOT EXISTS agentdata(ID INTEGER PRIMARY KEY, timestamp INTERGER, name TEXT, monitor TEXT, value REAL);'
        agentevents = 'CREATE TABLE IF NOT EXISTS agentevents(ID INTEGER PRIMARY KEY, timestamp INTERGER, name TEXT, monitor TEXT, message TEXT, status INTEGER, severity TEXT, processed INTERGER);'
        agentsystem = 'CREATE TABLE IF NOT EXISTS agentsystem(ID INTEGER PRIMARY KEY, timestamp INTERGER, name TEXT, ipaddress TEXT, platform TEXT, build TEXT, architecture TEXT, domain TEXT, processors INTEGER, memory REAL);'
        notifyrule = 'CREATE TABLE IF NOT EXISTS notifyrule(ID INTEGER PRIMARY KEY, name TEXT, email TEXT, agent TEXT, monitor TEXT, status INTEGER, severity TEXT, enabled INTERGER);'
        users = 'CREATE TABLE IF NOT EXISTS users (ID INTEGER PRIMARY KEY, user TEXT, password TEXT, role INTERGER);'
        self.cursor.executescript(agentdata + agentevents + agentsystem + notifyrule + users)
        self.con.commit()

    # User Queries
    def user_auth(self, user, encrypt_password):
        sql = "SELECT user, role from users where user=? AND password=?"
        self.cursor.execute(sql, (user, encrypt_password))
        result = self.cursor.fetchone()
        if not result is None:
            return result # qname
        
    def user_password_change(self, user, password):
        sql = "UPDATE users SET password=? WHERE user=?"
        self.cursor.execute(sql, (password, user))
        self.con.commit()

    def users_select(self):
        sql = "SELECT id, user FROM users order by user" 
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
        
    def user_select(self, id):
        sql = "SELECT id, user, role FROM users WHERE id=?" 
        self.cursor.execute(sql, (id,))
        result = self.cursor.fetchone()
        return result

    def user_create_admin(self, user, encrypt_pass, role):
        sql = "INSERT INTO users(ID, user, password, role)  VALUES (1,?, ?, ?) ON CONFLICT DO NOTHING;" # SELECT ?, ?, ? FROM DUAL WHERE NOT EXISTS (SELECT * from users WHERE user=?) LIMIT 1"
        self.cursor.execute(sql, (user, encrypt_pass, role))
        self.con.commit()
        
    def user_create(self, user, encrypt_pass, role):
        sql = "INSERT INTO users(user, password, role)  VALUES (?, ?, ?) ON CONFLICT DO NOTHING;" # SELECT ?, ?, ? FROM DUAL WHERE NOT EXISTS (SELECT * from users WHERE user=?) LIMIT 1"
        self.cursor.execute(sql, (user, encrypt_pass, role))
        self.con.commit()
        
    def user_edit_role(self, id, role):
        sql = "UPDATE users set role=? where id=?"
        self.cursor.execute(sql, (role, id))
        self.con.commit()
        
    def user_edit_password(self, id, encrypt_pass):
        sql = "UPDATE users set password=? where id=?"
        self.cursor.execute(sql, (encrypt_pass, id))
        self.con.commit()
        
    def user_delete(self, id):
        sql = "DELETE FROM users where id=?"
        self.cursor.execute(sql, (id))
        self.con.commit()

    def user_add(self, user, password, role):
        D = Data()
        encrypt_password = hashlib.sha224(password.encode()).hexdigest()
        D.create_user(user, encrypt_password, role)
    
    # Index Queries
    def index_availability(self):
        sql = "SELECT timestamp from agentsystem"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def index_device(self, name):
        sql = "SELECT id, timestamp, name, ipaddress, platform, build, architecture, domain, processors, memory FROM agentsystem WHERE name=? LIMIT 1"
        self.cursor.execute(sql, (name,))
        result = self.cursor.fetchone()
        return result

    def index_device_list(self, page_start, page_end):
        sql = "SELECT id, timestamp, name, ipaddress, platform, build, architecture, domain, processors, memory FROM agentsystem ORDER BY name LIMIT ?,?"
        self.cursor.execute(sql, (page_start, page_end))
        result = self.cursor.fetchall()
        return result

    def index_device_count(self):
        sql = "SELECT COUNT(id) as total FROM agentsystem"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result

    # Event Queries
    def event_totals(self, status):
        sql = "SELECT severity, count(severity) as total from agentevents WHERE status=? group by severity"
        self.cursor.execute(sql, (status,))
        result = self.cursor.fetchall()
        return result

    def events_status(self, status):
        sql = "SELECT id, timestamp, name, monitor, message, severity from agentevents where status=? order by id desc"
        self.cursor.execute(sql, (status,))
        result = self.cursor.fetchall()
        return result

    def event_change_status(self, id, status):
        sql = "UPDATE agentevents SET status=? where id=?"
        self.cursor.execute(sql, (status, id))
        self.con.commit()

    def events(self, status):
        sql = "SELECT id, timestamp, name, monitor, message, severity from agentevents where status=? order by id desc"
        self.cursor.execute(sql, (status,))
        result = self.cursor.fetchall()
        return result

    # Device Queries
    def search_devices(self, name):
        sql = f"SELECT name FROM agentsystem WHERE name LIKE '%{name}%'"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def device_system(self, name):
        sql = "SELECT id, timestamp, name, ipaddress, platform, build, architecture, domain, processors, memory FROM agentsystem WHERE name=? LIMIT 1"
        self.cursor.execute(sql, (name,))
        result = self.cursor.fetchone()
        return result

    def devices_select_all(self):
        sql = "SELECT id, timestamp, name, ipaddress, platform, build, architecture, domain, processors, memory FROM agentsystem ORDER BY name"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def device_data_latest(self, name):
        sql = "SELECT id, timestamp, name, monitor, value from agentdata where name=? and timestamp = (SELECT timestamp from agentdata where name=? order by id desc LIMIT 1)"
        self.cursor.execute(sql, (name, name))
        result = self.cursor.fetchall()
        return result

    def device_list(self, page_start, page_end):
        sql = "SELECT id, timestamp, name, ipaddress, platform, build, architecture, domain, processors, memory FROM agentsystem ORDER BY name LIMIT ?,?"
        self.cursor.execute(sql, (page_start, page_end))
        result = self.cursor.fetchall()
        return result

    def device_graph(self, name, monitor):
        sql = "SELECT id, timestamp, name, monitor, value from agentdata where name=? and monitor=? order by id desc LIMIT 61"
        self.cursor.execute(sql, (name, monitor))
        result = self.cursor.fetchall()
        return result

    def device_all(self):
        sql = "SELECT id, timestamp, name, ipaddress, platform, build, architecture, domain, processors, memory FROM agentsystem ORDER BY name"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    # Notify
    def notify_rules(self):
        sql = "SELECT id, name, email, agent, monitor, status, severity, enabled FROM notifyrule order by name"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
            
    def notify_rule(self, id):
        sql = "SELECT id, name, email, agent, monitor, status, severity, enabled FROM notifyrule WHERE id=?"
        self.cursor.execute(sql, (id,))
        result = self.cursor.fetchone()
        return result
        
    def notify_add(self, notify_name, notify_email, agent_name, agent_monitor, agent_status, agent_severity, notify_enabled):
        sql = "INSERT INTO notifyrule (name, email, agent, monitor, status, severity, enabled) VALUES (?,?,?,?,?,?,?)"
        self.cursor.execute(sql, (notify_name, notify_email, agent_name, agent_monitor, agent_status, agent_severity, notify_enabled))
        self.con.commit()
        
    def notify_edit(self, notify_name, notify_email, agent_name, agent_monitor, agent_status, agent_severity, notify_enabled):
        sql = "UPDATE notifyrule SET name=?, email=?, agent=?, monitor=?, status=?, severity=?, enabled=? WHERE name=?"
        self.cursor.execute(sql, (notify_name, notify_email, agent_name, agent_monitor, agent_status, agent_severity, notify_enabled, notify_name))
        self.con.commit()
        
    def notify_delete(self, id):
        sql = "DELETE FROM notifyrule where id=?"
        self.cursor.execute(sql, (id))
        self.con.commit()

    def notify_device_names(self):
        sql = "SELECT name FROM agentsystem ORDER by name"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
        