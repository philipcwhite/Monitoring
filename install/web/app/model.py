import pymysql 
import hashlib, datetime, math, socket, time

class Auth:
    def verify(self, user, password):
        D = Data()
        encrypt_password = hashlib.sha224(password.encode()).hexdigest()
        authuser = D.user_auth(user, encrypt_password)
        if authuser is None: return None
        else: return authuser

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
        D.user_create(user, encrypt_password, role)

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
            timestamp = int(i['timestamp'])
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
        agentevents = D.index_event_totals(1)
        for i in agentevents:
            sev = int(i['severity'])
            sev_tot = int(i['total'])
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
        agent_platform = agentsystem['platform']
        agent_architecture = agentsystem['architecture']
        agent_timestamp = agentsystem['timestamp']
        agent_processors = agentsystem['processors']
        agent_memory = str(agentsystem['memory'])[:-3]
        agent_perf = D.device_data_latest(name)
        for i in agent_perf:
            if i['monitor'] == 'perf.processor.percent.used' : cpu_perc = float(i['value'])
            if i['monitor'] == 'perf.memory.percent.used' : mem_perc = float(i['value']) #[:-2]
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
        icon = ''
        rows = []
        for i in agentsystem:
            row = {}
            row['date'] = str(datetime.datetime.fromtimestamp(int(i['timestamp'])))
            color = '93C54B'
            if (int(i['timestamp']) + uptime_check) < currenttime : color = 'D9534F'
            row['color'] = color
            row['name']= name
            row['ipaddress'] = str(i["ipaddress"])
            row['domain'] = str(i["domain"]).lower()
            row['platform'] = i["platform"]
            row['architecture'] = i["architecture"]
            rows.append(row)
        index_dict['host_summary'] = rows
        # Pager
        pager = ''
        agent_count = D.index_device_count()
        page_count = int(math.ceil(int(agent_count['total']) / 100))
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
            sev = int(i['severity'])
            sev_tot = int(i['total'])
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
            row['date'] = str(datetime.datetime.fromtimestamp(int(i['timestamp'])))
            row['name'] = i['name']
            row['message'] = i['message']
            row['id'] = str(i['id'])
            sev_text = ''
            if int(i['severity']) == 4:
                row['color'] = '#29ABE0'
                row['severity'] = 'Information'
            elif int(i['severity']) == 3:
                row['color']  = '#FFC107'
                row['severity'] = 'Warning'
            elif int(i['severity']) == 2:
                row['color']  = '#F47C3C'
                row['severity'] = 'Major'
            elif int(i['severity']) == 1:
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
            if (i['timestamp'] + uptime_check) >= currenttime: row['fill'] = '#93C54B'
            else: row['fill'] = '#d9534f'
            row['name'] = i['name']
            row['domain'] = i['domain']
            row['ipaddress'] = i['ipaddress']
            row['platform'] = i['platform']
            rows.append(row)
        return rows

    def device(self, name): 
        device_dict = {}
        D = Data()
        agentsystem = D.device_system(name)
        device_dict['ipaddress'] = agentsystem["ipaddress"]
        device_dict['domain'] = agentsystem["domain"].lower()
        device_dict['platform'] = agentsystem["platform"]
        device_dict['architecture'] = agentsystem["architecture"]
        device_dict['build'] = agentsystem["build"]
        device_dict['processors'] = str(agentsystem["processors"])
        device_dict['memory'] = str(agentsystem["memory"])[:-3]
        agent_query = D.device_data_latest(name)
        cpu_perc = mem_perc = pagefile_perc = uptime_days = net_br = net_bs = 0
        fs_list = []
        for i in agent_query:
            if i['monitor'] == 'perf.processor.percent.used': device_dict['cpu_perc'] = str(round(float(i['value']), 0))
            if i['monitor'] == 'perf.memory.percent.used': device_dict['mem_perc'] = str(round(float(i['value']), 0))
            if i['monitor'] == 'perf.pagefile.percent.used': device_dict['pagefile_perc'] = str(round(float(i['value']), 0))
            if i['monitor'] == 'perf.system.uptime.seconds': device_dict['uptime_days'] = str(round(float(i['value']) / 86400, 0))
            if i['monitor'] == 'perf.network.bytes.received': device_dict['net_br'] = str(round(float(i['value']), 0))
            if i['monitor'] == 'perf.network.bytes.sent': device_dict['net_bs'] = str(round(float(i['value']), 0))
            if 'filesystem' in i['monitor'] and 'percent.used' in i['monitor']:
                fs_name = i['monitor'].replace('perf.filesystem.','').replace('.percent.used','')
                fs = (fs_name, str(i['value']))
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
            if float(i['value']) > max_value:max_value = float(i['value'])          
        for i in device_data:
            device_value = float(i['value'])
            time_short = datetime.datetime.fromtimestamp(int(i['timestamp'])).strftime('%H:%M')
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
                last_reported = str(datetime.datetime.fromtimestamp(int(i['timestamp'])))
                output += last_reported + ',' + i['name'] + ',' + i['ipaddress'] + ',' + i['platform'] + ',' + str(i['build']) + ',' + i['architecture']
                output +=  ',' + i['domain'] + ',' + str(i['processors']) + ',' + str(i['memory']) + cr
        if name == 'events':
            events = D.events(1)
            output = 'Date, Name, Monitor, Message, Severity' + cr
            for i in events:
                last_reported = str(datetime.datetime.fromtimestamp(int(i['timestamp'])))
                output += last_reported + ',' + i['name'] + ',' + i['monitor'] + ',' + i['message'] + ',' + str(i['severity']) + cr
        return output

class Data:
    def __init__(self):
        self.con = pymysql.connect(host = 'localhost', user = 'monitoring', password = 'monitoring', db = 'monitoring', charset = 'utf8mb4', cursorclass = pymysql.cursors.DictCursor)
        self.cursor = self.con.cursor()

    def __del__(self):
        self.con.close()

    # User Queries
    '''def user_get(self, user, password):
        sql = 'SELECT id FROM users WHERE user=%s AND password=%s'
        self.cursor.execute(sql, (user, password))
        id = self.cursor.fetchone()
        if not id is None: return True'''

    def user_auth(self, user, encrypt_password):
        sql = "SELECT user, password from users where user=%s AND password=%s"
        self.cursor.execute(sql, (user, encrypt_password))
        result = self.cursor.fetchone()
        qname = ''
        if not result is None:
            qname = result['user']
            return qname
        
    def user_password_change(self, user, password):
        sql = "UPDATE users SET password=%s WHERE user=%s"
        self.cursor.execute(sql, (password, user))
        self.con.commit()

    def users_select(self):
        sql = "SELECT id, user FROM users order by user" 
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
        
    def user_select(self, id):
        sql = "SELECT id, user, role FROM users WHERE id=%s" 
        self.cursor.execute(sql, (id))
        result = self.cursor.fetchone()
        return result
        
    def user_create(self, user, encrypt_pass, role):
        sql = "INSERT INTO users (user, password, role) SELECT %s, %s, %s FROM DUAL WHERE NOT EXISTS (SELECT * from users WHERE user=%s) LIMIT 1"
        self.cursor.execute(sql, (user, encrypt_pass, role, user))
        self.con.commit()
        
    def user_edit_role(self, id, role):
        sql = "UPDATE users set role=%s where id=%s"
        self.cursor.execute(sql, (role, id))
        self.con.commit()
        
    def user_edit_password(self, id, encrypt_pass):
        sql = "UPDATE users set password=%s where id=%s"
        self.cursor.execute(sql, (encrypt_pass, id))
        self.con.commit()
        
    def user_delete(self, id):
        sql = "DELETE FROM users where id=%s"
        self.cursor.execute(sql, (id))
        self.con.commit()

    def user_add(user, password, role):
        D = Data()
        encrypt_password = hashlib.sha224(password.encode()).hexdigest()
        D.create_user(user, encrypt_password, role)
    
    # Index Queries
    def index_availability(self):
        sql = "SELECT timestamp from agentsystem"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def index_event_totals(self, status):
        sql = "SELECT severity, count(severity) as total from agentevents WHERE status=%s group by severity"
        self.cursor.execute(sql, (status))
        result = self.cursor.fetchall()
        return result

    def index_device(self, name):
        sql = "SELECT id, timestamp, name, ipaddress, platform, build, architecture, domain, processors, memory FROM agentsystem WHERE name=%s LIMIT 1"
        self.cursor.execute(sql, (name))
        result = self.cursor.fetchone()
        return result

    def index_device_list(self, page_start, page_end):
        sql = "SELECT id, timestamp, name, ipaddress, platform, build, architecture, domain, processors, memory FROM agentsystem ORDER BY name LIMIT %s,%s"
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
        sql = "SELECT severity, count(severity) as total from agentevents WHERE status=%s group by severity"
        self.cursor.execute(sql, (status))
        result = self.cursor.fetchall()
        return result

    def events_status(self, status):
        sql = "SELECT id, timestamp, name, monitor, message, severity from agentevents where status=%s order by id desc"
        self.cursor.execute(sql, (status))
        result = self.cursor.fetchall()
        return result

    def event_change_status(self, id, status):
        sql = "UPDATE agentevents SET status=%s where id=%s"
        self.cursor.execute(sql, (status, id))
        self.con.commit()

    def events(self, status):
        sql = "SELECT id, timestamp, name, monitor, message, severity from agentevents where status=%s order by id desc"
        self.cursor.execute(sql, (status))
        result = self.cursor.fetchall()
        return result

    # Device Queries
    def search_devices(self, name):
        sql = f"SELECT name FROM agentsystem WHERE name LIKE '%{name}%'"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def device_system(self, name):
        sql = "SELECT id, timestamp, name, ipaddress, platform, build, architecture, domain, processors, memory FROM agentsystem WHERE name=%s LIMIT 1"
        self.cursor.execute(sql, (name))
        result = self.cursor.fetchone()
        return result

    def devices_select_all(self):
        sql = "SELECT id, timestamp, name, ipaddress, platform, build, architecture, domain, processors, memory FROM agentsystem ORDER BY name"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def device_data_latest(self, name):
        sql = "SELECT id, timestamp, name, monitor, value from agentdata where name=%s and timestamp = (SELECT timestamp from agentdata where name=%s order by id desc LIMIT 1)"
        self.cursor.execute(sql, (name, name))
        result = self.cursor.fetchall()
        return result

    def device_list(self, page_start, page_end):
        sql = "SELECT id, timestamp, name, ipaddress, platform, build, architecture, domain, processors, memory FROM agentsystem ORDER BY name LIMIT %s,%s"
        self.cursor.execute(sql, (page_start, page_end))
        result = self.cursor.fetchall()
        return result

    def device_graph(self, name, monitor):
        sql = "SELECT id, timestamp, name, monitor, value from agentdata where name=%s and monitor=%s order by id desc LIMIT 61"
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
        sql = "SELECT id, notify_name, notify_email, agent_name, agent_monitor, agent_status, agent_severity, notify_enabled FROM notifyrule order by notify_name"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
            
    def notify_rule(self, id):
        sql = "SELECT id, notify_name, notify_email, agent_name, agent_monitor, agent_status, agent_severity, notify_enabled FROM notifyrule WHERE id=%s"
        self.cursor.execute(sql, (id))
        result = self.cursor.fetchone()
        return result
        
    def notify_add(self, notify_name, notify_email, agent_name, agent_monitor, agent_status, agent_severity, notify_enabled):
        sql = "INSERT INTO notifyrule (notify_name, notify_email, agent_name, agent_monitor, agent_status, agent_severity, notify_enabled) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(sql, (notify_name, notify_email, agent_name, agent_monitor, agent_status, agent_severity, notify_enabled))
        self.con.commit()
        
    def notify_edit(self, notify_name, notify_email, agent_name, agent_monitor, agent_status, agent_severity, notify_enabled):
        sql = "UPDATE notifyrule SET notify_name=%s, notify_email=%s, agent_name=%s, agent_monitor=%s, agent_status=%s, agent_severity=%s, notify_enabled=%s WHERE notify_name=%s"
        self.cursor.execute(sql, (notify_name, notify_email, agent_name, agent_monitor, agent_status, agent_severity, notify_enabled, notify_name))
        self.con.commit()
        
    def notify_delete(self, id):
        sql = "DELETE FROM notifyrule where id=%s"
        self.cursor.execute(sql, (id))
        self.con.commit()

    def notify_device_names(self):
        sql = "SELECT name FROM agentsystem ORDER by name"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
