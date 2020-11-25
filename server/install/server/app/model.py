import pymysql 
import hashlib, datetime, math, socket, time

class Auth:
    def verify(self, username, password):
        D = Data()
        encrypt_password = hashlib.sha224(password.encode()).hexdigest()
        authuser = D.user_auth(username, encrypt_password)
        if authuser is None: return None
        else: return authuser

    def user_password_change(self, username, pass1, pass2):
        D = Data()
        encrypt_password1 = hashlib.sha224(pass1.encode()).hexdigest()
        encrypt_password2 = hashlib.sha224(pass2.encode()).hexdigest()
        authuser = D.user_auth(username, encrypt_password1)
        if not authuser is None:
            D.user_password_change(username, encrypt_password2)
            return True
        return False

    def user_password_set(self, pass1, pass2):
        if pass1 == pass2:
            encrypt_password = hashlib.sha224(pass1.encode()).hexdigest()
            return encrypt_password

    def user_initialize(self):
        #Check if admin user exists. If not create it
        D = Data()
        username = 'admin'
        password = 'password'
        role = 1
        encrypt_password = hashlib.sha224(password.encode()).hexdigest()
        D.user_create(username, encrypt_password, role)

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
        rows = ''
        for i in agentsystem:
            dt = datetime.datetime.fromtimestamp(int(i['timestamp']))
            date = f'<span style="padding-right:10px">Last Reported: {str(dt)}</span>'
            color = '93C54B'
            if (int(i['timestamp']) + uptime_check) < currenttime : color = 'D9534F'
            icon = f'<svg width="10" height="10"><rect width="10" height="10" rx="2" ry="2" style="fill:#{color}" /></svg>'
            rows = f'<tr><td style="padding-left:20px">{icon} &nbsp;<a href="device/{str(i["name"])}">{str(i["name"])}</a></td><td>IP Address: {str(i["ipaddress"])}</td><td>Domain: {str(i["domain"]).lower()}</td><td>Platform: {str(i["platform"])} ({str(i["architecture"])})</td><td>{date}</td></tr>'
        index_dict['host_summary'] = rows

        # Pager
        pager = ''
        agent_count = D.index_device_count()
        page_count = int(math.ceil(int(agent_count['total']) / 100))
        if page_count > 1:
            for i in range(1,page_count + 1):
                if i == page: pager += f'<td style="width:10px">{str(i)}</td>'
                elif i == 1: pager += f'<td style="width:10px"><a href="/">{str(i)}</a></td>'
                else: pager += f'<td style="width:10px"><a href="/{str(i)}">{str(i)}</a></td>'
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

        events = ''
        agentevents = D.events_status(status)
        color = '#CCCCCC'
        change_status = abs(int(status) - 1)
        change_status_text = ""
        if change_status == 0: change_status_text = 'Close Event'
        else: change_status_text = 'Open Event'
        for i in agentevents:
            date = str(datetime.datetime.fromtimestamp(int(i['timestamp'])))
            sev_text = ''
            if int(i['severity']) == 4:
                color = '#29ABE0'
                sev_text = 'Information'
            elif int(i['severity']) == 3:
                color = '#FFC107'
                sev_text = 'Warning'
            elif int(i['severity']) == 2:
                color = '#F47C3C'
                sev_text = 'Major'
            elif int(i['severity']) == 1:
                color = '#D9534F'
                sev_text = 'Critical'
            events += f'<tr><td style="text-align:left;padding-left:10px">{date}</td>'
            events += f'<td style="text-align:left"><svg width="10" height="10"><rect width="10" height="10" rx="2" ry="2" style="fill:{color}" /></svg> {sev_text}</td><td><a href="device/{i["name"]}">{i["name"]}</a></td><td>{i["message"]}</td>'
            events += f'<td style="text-align:right;padding-right:12px"><input type="button" onclick="window.location.href=\'event_change/{str(i["id"])}/{str(change_status)}\'" class="action-button" value="{change_status_text}" /></td>'
            events += '</tr>'
        events_dict['event_list'] = events
        
        return events_dict

    def devices(self):    
        D = Data()
        agentsystem = D.devices_select_all()
        uptime_check = 600
        currenttime = time.time()
        device_list = icon = ''
        for i in agentsystem:
            if (i['timestamp'] + uptime_check) >= currenttime: icon = '<svg width="10" height="10"><rect width="10" height="10" rx="2" ry="2" style="fill:#93C54B" /></svg>'
            else: icon =  '<svg width="10" height="10"><rect width="10" height="10" rx="2" ry="2" style="fill:#d9534f" /></svg>'
            device_list += f'<tr><td style="padding-left:10px">{icon}</td><td><a href="device/{str(i["name"])}">{str(i["name"])}</td><td>{str(i["domain"])}</td><td>{str(i["ipaddress"])}</td><td>{str(i["platform"])}</td></tr>'
        return device_list

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


class Data:
    def __init__(self):
        self.con = pymysql.connect(host = 'localhost', user = 'monitoring', password = 'monitoring', db = 'monitoring', charset = 'utf8mb4', cursorclass = pymysql.cursors.DictCursor)
        self.cursor = self.con.cursor()

    def __del__(self):
        self.con.close()

    # User Queries
    def user_get(self, user, password):
        sql = 'SELECT id FROM users WHERE user=%s AND password=%s'
        self.cursor.execute(sql, (user, password))
        id = self.cursor.fetchone()
        if not id is None: return True

    def user_auth(self, username, encrypt_password):
        sql = "SELECT username, password from users where username=%s AND password=%s"
        self.cursor.execute(sql, (username, encrypt_password))
        result = self.cursor.fetchone()
        qname = ''
        if not result is None:
            qname = result['username']
            return qname
        
    def user_password_change(self, username, password):
        sql = "UPDATE users SET password=%s WHERE username=%s"
        self.cursor.execute(sql, (password, username))
        self.con.commit()

    def select_users(self):
        sql = "SELECT id, username FROM users order by username" 
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
        
    def user_select(self, id):
        sql = "SELECT id, username, role FROM users WHERE id=%s" 
        self.cursor.execute(sql, (id))
        result = self.cursor.fetchone()
        return result
        
    def user_create(self, username, encrypt_pass, role):
        sql = "INSERT INTO users (username, password, role) SELECT %s, %s, %s FROM DUAL WHERE NOT EXISTS (SELECT * from users WHERE username=%s) LIMIT 1"
        self.cursor.execute(sql, (username, encrypt_pass, role, username))
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

    def user_add(username, password, role):
        D = Data()
        encrypt_password = hashlib.sha224(password.encode()).hexdigest()
        D.create_user(username, encrypt_password, role)
    
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
