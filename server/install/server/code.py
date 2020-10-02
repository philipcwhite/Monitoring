import time, datetime, socket, math, hashlib 
from data import Data

class WebAuth:
    def verify_auth(username, password):
        WD = Data()
        encrypt_password = hashlib.sha224(password.encode()).hexdigest()
        authuser = WD.web_auth(username, encrypt_password)
        if authuser is None: return None
        else: return authuser

    def change_password(username, pass1, pass2):
        WD = Data()
        encrypt_password1 = hashlib.sha224(pass1.encode()).hexdigest()
        encrypt_password2 = hashlib.sha224(pass2.encode()).hexdigest()
        authuser = WD.web_auth(username, encrypt_password1)
        if not authuser is None:
            WD.change_password(username, encrypt_password2)
            return True
        return False

    def set_password(pass1, pass2):
        if pass1 == pass2:
            encrypt_password = hashlib.sha224(pass1.encode()).hexdigest()
            return encrypt_password

class WebCodeGraph:
    def __init__(self, time, dvalue):
        self.time=time
        self.dvalue=dvalue

class WebCode:
    def device_content_system(name):
        WD = Data()
        agentsystem = WD.device_system(name)
        html = '<table style="width:100%"><tr>'
        html += f'<td><b>Name:</b> {agentsystem["name"]}</td>'
        html += f'<td><b>IP Address:</b> {agentsystem["ipaddress"]}</td>'
        html += f'<td><b>Domain:</b> {agentsystem["domain"].lower()}</td>'
        html += f'<td><b>Platform:</b> {agentsystem["platform"]} ({agentsystem["architecture"]})</td>'
        html += f'<td><b>Build:</b> {str(agentsystem["build"])}</td>'
        html += f'<td><b>Processors:</b> {str(agentsystem["processors"])}</td>'
        html += f'<td><b>Memory:</b> {str(agentsystem["memory"])[:-3]} MB</td>'
        html += '</tr></table>'
        return html

    def device_content_data(name):  
        WD = Data()
        agentsystem = WD.device_system(name)
        agent_query = WD.device_data_latest(name)
        cpu_perc = mem_perc = pagefile_perc = uptime_days = net_br = net_bs = 0
        fs_list = []
        for i in agent_query:
            if i['monitor'] == 'perf.processor.percent.used': cpu_perc = round(float(i['value']), 0)
            if i['monitor'] == 'perf.memory.percent.used': mem_perc = round(float(i['value']), 0)
            if i['monitor'] == 'perf.pagefile.percent.used': pagefile_perc = round(float(i['value']), 0)
            if i['monitor'] == 'perf.system.uptime.seconds': uptime_days = round(float(i['value']) / 86400, 0)
            if i['monitor'] == 'perf.network.bytes.received': net_br = round(float(i['value']), 0)
            if i['monitor'] == 'perf.network.bytes.sent': net_bs = round(float(i['value']), 0)
            if 'filesystem' in i['monitor'] and 'percent.used' in i['monitor']:
                fs_name = i['monitor'].replace('perf.filesystem.','').replace('.percent.used','')
                fs_list.append(fs_name)
        html_fs = '<tr><td  style="padding-bottom:4px;text-align:left">'
        html_fs += '<div class="card-div">'
        html_fs += '<div class="card-header">Filesystem Monitors</div>'
        html_fs += '<div style="padding-left: 10px">'
        for i in fs_list:
            try:
                fs_query_used = WD.device_filesystem(name, 'perf.filesystem.' + i + '.percent.used')
                fs_used = str(round(float(fs_query_used['value']),0))
                fs_name = ''
                if agentsystem['platform'] == 'Windows':
                    fs_query_active = WD.device_filesystem(name,'perf.filesystem.' + i + '.percent.active')
                    fs_active = str(round(float(fs_query_active['value']),0))
                    fs_name = f'Windows {i} drive'
                    html_fs += f'<table style="width:100%"><tr><td style="width:33%">{fs_name}</td>'
                    html_fs += f'<td style="width:33%"><a href="/devices/{name}/perf.filesystem.{i}.percent.used">Space Used: {fs_used}</a></td>'
                    html_fs += f'<td style="width:33%"><a href="/devices/{name}/perf.filesystem.{i}.percent.active">Filesystem Activity: {fs_active}</a></td>'
                    html_fs += '<td style="width:33%"></td></tr></table>'
                elif agentsystem['platform'] == 'Linux':
                    fs_name = f'Linux Filesystem: {i}'   
                    html_fs += f'<table style="width:100%"><tr><td style="width:33%">{fs_name}</td>'
                    html_fs += f'<td style="width:33%"><a href="/devices/{name}/perf.filesystem.{i}.percent.used">Space Used: {fs_used}</a></td>'
                    html_fs += '<td style="width:33%"></td></tr></table>'
            except: pass
        html_fs += '</div></div></td></tr>' 
        html = '<tr><td style="padding-right:4px;text-align:center">'
        html += '<div class="card-div" style="height:70px"><div class="card-header">Processor (% used)</div>'
        html += f'<div  class="device-stats"><a class="device-stats" href="/devices/{name}/perf.processor.percent.used">{str(cpu_perc)}</a></div>'
        html += '</div></td>'
        html += '<td style="padding-left:4px;padding-right:4px;text-align:center">'
        html += '<div class="card-div" style="height:70px"><div class="card-header">Memory (% used)</div>'
        html += f'<span class="device-stats"><a class="device-stats" href="/devices/{name}/perf.memory.percent.used">{str(mem_perc)}</a></span>'
        html += '</div></td>'
        html += '<td style="padding-left:4px;padding-right:4px;text-align:center">'
        html += '<div class="card-div" style="height:70px"><div class="card-header">Pagefile (% used)</div>'
        html += f'<span class="device-stats"><a class="device-stats" href="/devices/{name}/perf.pagefile.percent.used">{str(pagefile_perc)}</a></span>'
        html += '</div></td>'
        html += '<td style="padding-left:4px;text-align:center">'
        html += '<div class="card-div" style="height:70px"><div class="card-header">Uptime (days)</div>'
        html += f'<span class="device-stats"><a class="device-stats" href="/devices/{name}/perf.system.uptime.seconds">{str(uptime_days)}</a></span>'
        html += '</div></td></tr></table>'
        html += '<table style="width:100%">'
        html += '<tr><td style="padding-bottom:4px;text-align:left">'
        html += '<div class="card-div"><div class="card-header">Network Monitors</div><div style="padding-left: 10px">'
        html += '<table style="width:100%"><tr>'
        html += '<td style="width:33%">Network Total Traffic</td>'
        html += f'<td style="width:33%"><a href="/devices/{name}/perf.network.bytes.sent">Bytes Sent: {str(net_bs)}</a></td>'
        html += f'<td style="width:33%"><a href="/devices/{name}/perf.network.bytes.received">Bytes Received: {str(net_br)}</a></td>'
        html += '</tr></table></div></div></td></tr>'
        html += html_fs
        return html

    def device_content(name):
        html = '<table style="width:100%;">'
        html += '<tr><td colspan="4" style="padding-bottom:4px;text-align:left">'
        html += '<div class="card-div" style="height:45px">'
        html += '<div class="card-header">System Information</div>'
        html += f'<div style="padding-left: 10px">{WebCode.device_content_system(name)}'
        html += f'</div></div></td></tr>{WebCode.device_content_data(name)}</table>'
        return html

    def device_graph(name, monitor):
        WD = Data()
        device_data = WD.device_graph(name, monitor)
        data_list = []
        max_value = 0
        graph_time = datetime.datetime.now() - datetime.timedelta(minutes=60)
        for i in range(61):
            agent_data = WebCodeGraph(time=graph_time.strftime('%H:%M'),dvalue=0)
            data_list.append(agent_data)
            graph_time = graph_time + datetime.timedelta(minutes=1)
        for i in device_data:
            if float(i['value']) > max_value:max_value = float(i['value'])          
        for i in device_data:
            device_value = float(i['value'])
            time_short = datetime.datetime.fromtimestamp(int(i['timestamp'])).strftime('%H:%M')
            for i in data_list:
                if i.time == time_short:
                    if device_value == 0: i.dvalue = 0
                    else: i.dvalue = (device_value / max_value)*100
        device_polyline = ''
        device_polyline_data = ''
        device_time = ''
        xvalue = 55
        time_x = 0
        for i in data_list:
            dvalue = str(round(110 - i.dvalue))
            device_polyline_data += str(xvalue) + ',' + dvalue + ' '
            time_x += 1
            if time_x == 1:
                device_time += f'<text x="{str(xvalue)}" y="130" fill="#8E8C84" text-anchor="middle">{str(i.time)}</text>'
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

    def device_index():
        WD = Data()
        agentsystem = WD.device_all()
        uptime_check = 600
        currenttime = time.time()
        html = icon = ''
        for i in agentsystem:
            if (i['timestamp'] + uptime_check) >= currenttime: icon = '<svg width="10" height="10"><rect width="10" height="10" rx="2" ry="2" style="fill:#93C54B" /></svg>'
            else: icon =  '<svg width="10" height="10"><rect width="10" height="10" rx="2" ry="2" style="fill:#d9534f" /></svg>'
            html += f'<tr><td style="padding-left:10px">{icon}</td><td><a href="/devices/{str(i["name"])}">{str(i["name"])}</td><td>{str(i["domain"])}</td><td>{str(i["ipaddress"])}</td><td>{str(i["platform"])}</td></tr>'
        return html

    def search_devices(device):
        WD = Data()
        results = WD.device_system_search(device)
        html = "Host names containing: " + str(device) + "<br />"
        for i in results:
            html += f'<a href="/devices/{str(i["name"])}/">{str(i["name"])}</a></br />'
        return html

    def index(page):
        WD = Data()
        block1 = block2 = block3 = block4 = pager = ''
        # Block 1
        ok = down = 0
        total = ok + down
        uptime_check = 300
        currenttime = time.time()
        agentsystem = WD.index_device_avail()
        for i in agentsystem:
            timestamp = int(i['timestamp'])
            if (timestamp + uptime_check) >= currenttime: ok += 1
            else: down += 1
        total = ok + down
        if total == 0: total = 1
        ok_perc = (ok / total) * 100
        down_perc = (down / total) * 100
        total_perc = str(ok_perc) + ' ' + str(down_perc)
        block1 = '<table style="width:100%;height:105px"><tr><td style="width:50%;text-align:center;">'
        block1 += '<svg width="95" height="95" viewBox="0 0 42 42" class="donut">'
        block1 += '<circle class="donut-ring" cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#d9534f" stroke-width="5"></circle>'
        block1 += f'<circle class="donut-segment" cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#93C54B" stroke-width="5" stroke-dasharray="{total_perc}" stroke-dashoffset="25"></circle></svg></td>'
        block1 += '<td style="width:50%;vertical-align:top;text-align:left;padding-top:34px">'
        block1 += f'<svg width="10" height="10"><rect width="10" height="10" rx="2" ry="2" style="fill:#93C54B" /></svg> {str(ok)} Hosts Up<br />'
        block1 += f'<svg width="10" height="10"><rect width="10" height="10" rx="2" ry="2" style="fill:#d9534f" /></svg> {str(down)} Hosts Down</td></tr></table>'
        # Block 2
        info = warn = majr = crit = 0
        agentevents = WD.event_totals(1)
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
        info_points = str(info_perc) + ' ' + str(100 - info_perc)
        warn_points = str(warn_perc) + ' ' + str(100 - warn_perc)
        majr_points = str(majr_perc) + ' ' + str(100 - majr_perc)
        crit_points = str(crit_perc) + ' ' + str(100 - crit_perc)
        block2 = '<table style="width:100%;height:105px"><tr><td style="width:50%;text-align:center">'
        block2 += '<svg width="95" height="95" viewBox="0 0 42 42" class="donut">'
        block2 += f'<circle class="donut-ring" cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#93C54B" stroke-width="5"></circle>'
        block2 += f'<circle class="donut-segment" cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#29ABE0" stroke-width="5" stroke-dasharray="{info_points}" stroke-dashoffset="25"></circle>'
        block2 += f'<circle class="donut-segment" cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#ffc107" stroke-width="5" stroke-dasharray="{warn_points}" stroke-dashoffset="{str(100 - info_perc + 25)}"></circle>'
        block2 += f'<circle class="donut-segment" cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#F47C3C" stroke-width="5" stroke-dasharray="{majr_points}" stroke-dashoffset="{str(100 - info_perc - warn_perc + 25)}"></circle>'
        block2 += f'<circle class="donut-segment" cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#d9534f" stroke-width="5" stroke-dasharray="{crit_points}" stroke-dashoffset="{str(100 - info_perc - warn_perc - majr_perc + 25)}"></circle>'
        block2 += '</svg></td><td style="width:50%;vertical-align:top;text-align:left;padding-top:16px">'
        block2 += f'<svg width="10" height="10"><rect width="10" height="10" rx="2" ry="2" style="fill:#29ABE0" /></svg> {str(info)} Information<br />'
        block2 += f'<svg width="10" height="10"><rect width="10" height="10" rx="2" ry="2" style="fill:#ffc107" /></svg> {str(warn)} Warning<br />'
        block2 += f'<svg width="10" height="10"><rect width="10" height="10" rx="2" ry="2" style="fill:#F47C3C" /></svg> {str(majr)} Major<br />'
        block2 += f'<svg width="10" height="10"><rect width="10" height="10" rx="2" ry="2" style="fill:#d9534f" /></svg> {str(crit)} Critical'
        block2 += '</td></tr></table>'
        # Block 3
        name = socket.gethostname().lower()
        uptime_check = 300
        currenttime = time.time()
        agent_platform = agent_architecture = ''
        agent_timestamp = agent_processors = agent_memory = cpu_perc = mem_perc = 0
        try:
            agentsystem = WD.device_system(name)
            agent_platform = agentsystem['platform']
            agent_architecture = agentsystem['architecture']
            agent_timestamp = agentsystem['timestamp']
            agent_processors = agentsystem['processors']
            agent_memory = agentsystem['memory']
            agent_perf = WD.device_data_latest(name)
            for i in agent_perf:
                if i['monitor'] == 'perf.processor.percent.used' : cpu_perc = float(i['value'])
                if i['monitor'] == 'perf.memory.percent.used' : mem_perc = float(i['value'])
        except: pass
        block3 = '<table style="width:100%;height:105px;padding-top:6px;padding-left:10px"><tr><td style="width:50%;vertical-align:top;text-align:left">'
        block3 += f'Name: {name}<br />'
        block3 += f'Processors: {str(agent_processors)}<br />'
        block3 += f'Memory: {str(agent_memory)[:-3]} MB <br />'
        block3 += f'Platform: {agent_platform} ({agent_architecture})<br />'
        block3 += '</td><td style="width:50%;vertical-align:top;text-align:left">'
        if (agent_timestamp + uptime_check) >= currenttime:
            cpu_color = mem_color = '93C54B'
            if cpu_perc >= 90 : cpu_color = 'D9534F'
            block3 += f'<svg width="10" height="10"><rect width="10" height="10" rx="2" ry="2" style="fill:#{cpu_color}" /></svg> {str(cpu_perc)[:-2]}% CPU<br />'
            if mem_perc >= 90: mem_color = 'D9534F'
            block3 += f'<svg width="10" height="10"><rect width="10" height="10" rx="2" ry="2" style="fill:#{mem_color}" /></svg> {str(mem_perc)[:-2]}% Memory<br />'
        else: block3 += 'Agent Not Reporting'
        block3 += '</td></tr></table>'
        # Block 4
        page_start = (int(page) * 100) - 100
        page_end = page_start + 100
        agentsystem = WD.index_devices(page_start, page_end)
        uptime_check = 300
        currenttime = time.time()
        icon = ''
        for i in agentsystem:
            dt = datetime.datetime.fromtimestamp(int(i['timestamp']))
            date = f'<span style="padding-right:10px">Last Reported: {str(dt)}</span>'
            color = '93C54B'
            if (int(i['timestamp']) + uptime_check) < currenttime : color = 'D9534F'
            icon = f'<svg width="10" height="10"><rect width="10" height="10" rx="2" ry="2" style="fill:#{color}" /></svg>'
            block4 = f'<tr><td style="padding-left:20px">{icon} &nbsp;<a href="devices/{str(i["name"])}">{str(i["name"])}</a></td><td>IP Address: {str(i["ipaddress"])}</td><td>Domain: {str(i["domain"]).lower()}</td><td>Platform: {str(i["platform"])} ({str(i["architecture"])})</td><td>{date}</td></tr>'
        # Pager
        page_start = (int(page) * 100) - 100
        page_end = page_start + 100
        agent_count = WD.index_device_count()
        page_count = int(math.ceil(int(agent_count['total']) / 100))
        if page_count > 1:
            for i in range(1,page_count + 1):
                if i == page: pager += f'<td style="width:10px">{str(i)}</td>'
                elif i == 1: pager += f'<td style="width:10px"><a href="/">{str(i)}</a></td>'
                else: pager += f'<td style="width:10px"><a href="/{str(i)}">{str(i)}</a></td>'
        return 'Host Availability', block1, 'Open Events', block2, 'Monitoring Server', block3, 'Host Summary', block4, pager

    def events(status):
        WD = Data()
        total = info = warn = majr = crit = 0
        agentevents = WD.event_totals(status)
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
        html = '<table style="width:100%;"><tr><td><div class="card-div">'
        html += '<div class="card-header">Event Summary</div><table style="width:100%;text-align:center"><tr>'
        html += f'<td style="text-align:left; padding-left:10px">{status_text}</td>'
        html += f'<td><svg width="10" height="10"><rect width="10" height="10" rx="2" ry="2" style="fill:#CCCCCC" /></svg>&nbsp; {str(total)}&nbsp;  Total</td>'
        html += f'<td><svg width="10" height="10"><rect width="10" height="10" rx="2" ry="2" style="fill:#29ABE0" /></svg>&nbsp;  {str(info)}&nbsp;  Information</td>'
        html += f'<td><svg width="10" height="10"><rect width="10" height="10" rx="2" ry="2" style="fill:#FFC107" /></svg>&nbsp;  {str(warn)}&nbsp;  Warning</td>'
        html += f'<td><svg width="10" height="10"><rect width="10" height="10" rx="2" ry="2" style="fill:#F47C3C" /></svg>&nbsp;  {str(majr)}&nbsp;  Major</td>'
        html += f'<td><svg width="10" height="10"><rect width="10" height="10" rx="2" ry="2" style="fill:#D9534F" /></svg>&nbsp;  {str(crit)}&nbsp;  Critical</td>'
        html += f'<td style="text-align:right;padding-right:12px"><input type="button" onclick="window.location.href=\'/events/?status={str(change_status)}\'" class="action-button" value={change_status_text} /></td>'
        html += '</tr></table></div></td></tr><tr><td style="text-align: left;padding-top:8px">'
        html += '<div class="card-div"><div class="card-header">Events</div><table style="width:100%">'
        agentevents = WD.events(status)
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
            html += f'<tr><td style="text-align:left;padding-left:10px">{date}</td>'
            html += f'<td style="text-align:left"><svg width="10" height="10"><rect width="10" height="10" rx="2" ry="2" style="fill:{color}" /></svg> {sev_text}</td><td><a href="/devices/{i["name"]}">{i["name"]}</a></td><td>{i["message"]}</td>'
            html += f'<td style="text-align:right;padding-right:12px"><input type="button" onclick="window.location.href=\'/event_change/{str(i["id"])}/{str(change_status)}\'" class="action-button" value="{change_status_text}" /></td>'
            html += '</tr>'
        html += '</table></div></td></tr></table>'
        return html

    def user_initialize():
        #Check if admin user exists. If not create it
        WD = Data()
        username = 'admin'
        password = 'password'
        role = 1
        encrypt_password = hashlib.sha224(password.encode()).hexdigest()
        WD.create_user(username, encrypt_password, role)

    def user_list():
        WD = Data()
        users = WD.select_users()
        html = "<table style='width:100%'>"
        for i in users:
            html += "<tr><td>" + str(i["username"]) + """</td><td style='text-align:right'><input type="button" onclick="window.location.href='/user_edit_pass/""" + str(i["id"]) + """'" class="action-button" value="Password" />
            <input type="button" onclick="window.location.href='/user_edit_role/""" + str(i["id"]) + """'" class="action-button" value="Roles" />
            <input type="button" onclick="window.location.href='/user_delete/""" + str(i["id"]) + """'" class="action-button" value="Delete" />
            </td></tr>"""
        html += """</table><input type="button" onclick="window.location.href='/user_add/'" class="action-button" value="Add User" />"""
        return html

    def user_add(username, password, role):
        WD = Data()
        encrypt_password = hashlib.sha224(password.encode()).hexdigest()
        WD.create_user(username, encrypt_password, role)

    def report_devices(ext):
        WD = Data()
        cr = ''
        if ext == 'html': cr = '<br />'
        elif ext == 'csv': cr = '\r\n'
        devices = WD.device_all()
        output = 'Last Reported,Name,IP Address,Platform,Build Number,Architecture,Domain,Processors,Memory' + cr
        for i in devices:
            last_reported = str(datetime.datetime.fromtimestamp(int(i['timestamp'])))
            output += last_reported + ',' + i['name'] + ',' + i['ipaddress'] + ',' + i['platform'] + ',' + str(i['build']) + ',' + i['architecture']
            output +=  ',' + i['domain'] + ',' + str(i['processors']) + ',' + str(i['memory']) + cr
        return output

    def report_events(ext):
        WD = Data()
        cr = ''
        if ext == 'html': cr = '<br />'
        elif ext == 'csv': cr = '\r\n'
        events = WD.events(1)
        output = 'Date, Name, Monitor, Message, Severity' + cr
        for i in events:
            last_reported = str(datetime.datetime.fromtimestamp(int(i['timestamp'])))
            output += last_reported + ',' + i['name'] + ',' + i['monitor'] + ',' + i['message'] + ',' + str(i['severity']) + cr
        return output

    def breadcrumbs(name, *args):
        html = ''
        if name == 'home':
            html = '<svg class="bread-font" viewBox="0 0 576 512"><path fill="currentColor" d="M488 312.7V456c0 13.3-10.7 24-24 24H348c-6.6 0-12-5.4-12-12V356c0-6.6-5.4-12-12-12h-72c-6.6 0-12 5.4-12 12v112c0 6.6-5.4 12-12 12H112c-13.3 0-24-10.7-24-24V312.7c0-3.6 1.6-7 4.4-9.3l188-154.8c4.4-3.6 10.8-3.6 15.3 0l188 154.8c2.7 2.3 4.3 5.7 4.3 9.3zm83.6-60.9L488 182.9V44.4c0-6.6-5.4-12-12-12h-56c-6.6 0-12 5.4-12 12V117l-89.5-73.7c-17.7-14.6-43.3-14.6-61 0L4.4 251.8c-5.1 4.2-5.8 11.8-1.6 16.9l25.5 31c4.2 5.1 11.8 5.8 16.9 1.6l235.2-193.7c4.4-3.6 10.8-3.6 15.3 0l235.2 193.7c5.1 4.2 12.7 3.5 16.9-1.6l25.5-31c4.2-5.2 3.4-12.7-1.7-16.9z"></path></svg>&nbsp;&nbsp;Home&nbsp;'  
        elif name == 'devices':
            html = '<svg class="bread-font" viewBox="0 0 512 512"><path fill="currentColor" d="M480 160H32c-17.673 0-32-14.327-32-32V64c0-17.673 14.327-32 32-32h448c17.673 0 32 14.327 32 32v64c0 17.673-14.327 32-32 32zm-48-88c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24zm-64 0c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24zm112 248H32c-17.673 0-32-14.327-32-32v-64c0-17.673 14.327-32 32-32h448c17.673 0 32 14.327 32 32v64c0 17.673-14.327 32-32 32zm-48-88c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24zm-64 0c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24zm112 248H32c-17.673 0-32-14.327-32-32v-64c0-17.673 14.327-32 32-32h448c17.673 0 32 14.327 32 32v64c0 17.673-14.327 32-32 32zm-48-88c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24zm-64 0c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24z"></path></svg>&nbsp;&nbsp;Devices&nbsp;&nbsp;'   
        elif name == 'device':
            html = f'<svg class="bread-font" viewBox="0 0 512 512"><path fill="currentColor" d="M480 160H32c-17.673 0-32-14.327-32-32V64c0-17.673 14.327-32 32-32h448c17.673 0 32 14.327 32 32v64c0 17.673-14.327 32-32 32zm-48-88c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24zm-64 0c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24zm112 248H32c-17.673 0-32-14.327-32-32v-64c0-17.673 14.327-32 32-32h448c17.673 0 32 14.327 32 32v64c0 17.673-14.327 32-32 32zm-48-88c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24zm-64 0c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24zm112 248H32c-17.673 0-32-14.327-32-32v-64c0-17.673 14.327-32 32-32h448c17.673 0 32 14.327 32 32v64c0 17.673-14.327 32-32 32zm-48-88c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24zm-64 0c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24z"></path></svg>&nbsp;&nbsp;<a href="/devices">Devices</a>&nbsp;>&nbsp;{args[0]}&nbsp;' 
        elif name == 'device_graph':
            html = '<svg class="bread-font" viewBox="0 0 512 512"><path fill="currentColor" d="M480 160H32c-17.673 0-32-14.327-32-32V64c0-17.673 14.327-32 32-32h448c17.673 0 32 14.327 32 32v64c0 17.673-14.327 32-32 32zm-48-88c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24zm-64 0c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24zm112 248H32c-17.673 0-32-14.327-32-32v-64c0-17.673 14.327-32 32-32h448c17.673 0 32 14.327 32 32v64c0 17.673-14.327 32-32 32zm-48-88c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24zm-64 0c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24zm112 248H32c-17.673 0-32-14.327-32-32v-64c0-17.673 14.327-32 32-32h448c17.673 0 32 14.327 32 32v64c0 17.673-14.327 32-32 32zm-48-88c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24zm-64 0c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24-10.745-24-24-24z"></path></svg>'
            html += f'&nbsp;&nbsp;<a href="/devices">Devices</a>&nbsp;>&nbsp;<a href="/devices/{args[0]}">{args[0]}</a>&nbsp;>&nbsp;{args[1]}&nbsp;'
        elif name == 'events':
            html = '<svg class="bread-font" viewBox="0 0 576 512"><path fill="currentColor" d="M569.517 440.013C587.975 472.007 564.806 512 527.94 512H48.054c-36.937 0-59.999-40.055-41.577-71.987L246.423 23.985c18.467-32.009 64.72-31.951 83.154 0l239.94 416.028zM288 354c-25.405 0-46 20.595-46 46s20.595 46 46 46 46-20.595 46-46-20.595-46-46-46zm-43.673-165.346l7.418 136c.347 6.364 5.609 11.346 11.982 11.346h48.546c6.373 0 11.635-4.982 11.982-11.346l7.418-136c.375-6.874-5.098-12.654-11.982-12.654h-63.383c-6.884 0-12.356 5.78-11.981 12.654z"></path></svg>&nbsp;&nbsp;Events&nbsp;'
        elif name == 'reports':
            html = '<svg class="bread-font" viewBox="0 0 512 512"><path fill="currentColor" d="M500 384c6.6 0 12 5.4 12 12v40c0 6.6-5.4 12-12 12H12c-6.6 0-12-5.4-12-12V76c0-6.6 5.4-12 12-12h40c6.6 0 12 5.4 12 12v308h436zM372.7 159.5L288 216l-85.3-113.7c-5.1-6.8-15.5-6.3-19.9 1L96 248v104h384l-89.9-187.8c-3.2-6.5-11.4-8.7-17.4-4.7z"></path></svg>&nbsp;&nbsp;Reports&nbsp;' 
        elif name == 'settings':
            html = '<svg class="bread-font" viewBox="0 0 512 512"><path fill="currentColor" d="M444.788 291.1l42.616 24.599c4.867 2.809 7.126 8.618 5.459 13.985-11.07 35.642-29.97 67.842-54.689 94.586a12.016 12.016 0 0 1-14.832 2.254l-42.584-24.595a191.577 191.577 0 0 1-60.759 35.13v49.182a12.01 12.01 0 0 1-9.377 11.718c-34.956 7.85-72.499 8.256-109.219.007-5.49-1.233-9.403-6.096-9.403-11.723v-49.184a191.555 191.555 0 0 1-60.759-35.13l-42.584 24.595a12.016 12.016 0 0 1-14.832-2.254c-24.718-26.744-43.619-58.944-54.689-94.586-1.667-5.366.592-11.175 5.459-13.985L67.212 291.1a193.48 193.48 0 0 1 0-70.199l-42.616-24.599c-4.867-2.809-7.126-8.618-5.459-13.985 11.07-35.642 29.97-67.842 54.689-94.586a12.016 12.016 0 0 1 14.832-2.254l42.584 24.595a191.577 191.577 0 0 1 60.759-35.13V25.759a12.01 12.01 0 0 1 9.377-11.718c34.956-7.85 72.499-8.256 109.219-.007 5.49 1.233 9.403 6.096 9.403 11.723v49.184a191.555 191.555 0 0 1 60.759 35.13l42.584-24.595a12.016 12.016 0 0 1 14.832 2.254c24.718 26.744 43.619 58.944 54.689 94.586 1.667 5.366-.592 11.175-5.459 13.985L444.788 220.9a193.485 193.485 0 0 1 0 70.2zM336 256c0-44.112-35.888-80-80-80s-80 35.888-80 80 35.888 80 80 80 80-35.888 80-80z"></path></svg>&nbsp;&nbsp;Settings&nbsp;' 
        return html
    
    def load_user_edit_role(role):
        html = """
        <form action="" method="POST">
        <table>
        <tr><td>Role</td>
        <td>"""
        if role == 0: html += "<input type='radio' name='role' value='0' checked='checked' /> User<input type='radio' name='role' value='1' /> Admin" 
        else: html += "<input type='radio' name='role' value='0' /> User<input type='radio' name='role' value='1' checked='checked' /> Admin"
        html += """</td></tr>
        <tr><td></td><td style="text-align:right"><input type="submit" class="action-button" value="Submit" /></td></tr>
        </table>
        </form>"""
        return html

    def notify_rules():
        WD = Data()
        notifyrules = WD.select_notifyrules()
        html = "<table style='width:100%'>"
        for i in notifyrules:
            html += "<tr><td>" + str(i["notify_name"]) + """</td><td style='text-align:right;padding-right:10px'> <input type="button" onclick="window.location.href='/notify_edit/""" + str(i["id"]) + """'" class="action-button" value="Edit" />
            <input type="button" onclick="window.location.href='/notify_delete/""" + str(i["id"]) + """'" class="action-button" value="Delete" /></td></tr>"""
        html += """</table><br /><input type="button" onclick="window.location.href='/notify_add/'" class="action-button" value="Add Notification Rule" />"""
        return html

    def notify_add():
        WD = Data()
        html = """<form action='' method='POST'><table><tr><td>Rule Name</td><td><input type='text' name='notify_name' /></td></tr>
               <tr><td>Email Address</td><td><input type='text' name='notify_email' /></td></tr>"""
        dd_html = "<tr><td>Hostname</td><td><select name='agent_name'><option value='%_%'>All</option>"
        hostnames = WD.device_system_names()
        for i in hostnames:
            dd_html += "<option value='" + str(i["name"]) + "'>" + str(i["name"]) + "</option>"
        dd_html += "</select></td></tr>"
        html += dd_html
        html += "<tr><td>Monitor</td><td><input type='text' name='agent_monitor' /></td></tr>"
        html += "<tr><td>Status</td><td><input type='radio' name='agent_status' value='1' /> Open <input type='radio' name='agent_status' value='0' /> Closed</td></tr>"
        html += "<tr><td>Severity</td><td><select name='agent_severity'><option value='4'>Information</option><option value='3'>Warning</option><option value='2'>Major</option><option value='1'>Critical</option>"
        html += "<tr><td>Enabled</td><td><input type='radio' name='notify_enabled' value='1' /> True <input type='radio' name='notify_enabled' value='0' /> False</td></tr>"
        html += "<tr><td></td><td style='text-align:right'><input type='submit' class='action-button' value='submit' /></td></tr></table>"
        return html
    
    def notify_edit(id):
        WD = Data()
        rule = WD.select_notifyrule(id)
        html = """<form action='' method='POST'><table><tr><td>Rule Name</td><td><input type='text' name='notify_name' value='""" + str(rule['notify_name']) + """' /></td></tr>
               <tr><td>Email Address</td><td><input type='text' name='notify_email'  value='""" + str(rule['notify_email']) + """' /></td></tr>"""
        html += "<tr><td>Hostname</td><td><input type='text' name='agent_name' value='" + str(rule['agent_name']) + "' /></td></tr>"
        html += "<tr><td>Monitor</td><td><input type='text' name='agent_monitor' value='" + str(rule['agent_monitor']) + "' /></td></tr>"
        if int(rule['agent_status']) == 1: html += "<tr><td>Status</td><td><input type='radio' name='agent_status' value='1' checked='checked' /> Open <input type='radio' name='agent_status' value='0' /> Closed</td></tr>"
        else: html += "<tr><td>Status</td><td><input type='radio' name='agent_status' value='1' /> Open <input type='radio' name='agent_status' value='0' checked='checked' /> Closed</td></tr>"
        html += "<tr><td>Severity</td><td><select name='agent_severity'>"
        if int(rule['agent_severity']) == 4: html += "<option value='4' selected>Information</option><option value='3'>Warning</option><option value='2'>Major</option><option value='1'>Critical</option>"
        elif int(rule['agent_severity']) == 3: html += "<option value='4'>Information</option><option value='3' selected>Warning</option><option value='2'>Major</option><option value='1'>Critical</option>"
        elif int(rule['agent_severity']) == 2: html += "<option value='4'>Information</option><option value='3'>Warning</option><option value='2' selected>Major</option><option value='1'>Critical</option>"
        elif int(rule['agent_severity']) == 1: html += "<option value='4'>Information</option><option value='3'>Warning</option><option value='2'>Major</option><option value='1' selected>Critical</option>"
        if int(rule['notify_enabled']) == 1: html += "<tr><td>Enabled</td><td><input type='radio' name='notify_enabled' value='1' checked='checked' /> True <input type='radio' name='Notify_Enabled' value='0' /> False</td></tr>"
        else: html += "<tr><td>Enabled</td><td><input type='radio' name='notify_enabled' value='1' /> True <input type='radio' name='notify_enabled' value='0' checked='checked' /> False</td></tr>"      
        html += "<tr><td></td><td style='text-align:right'><input type='submit' class='action-button' value='submit' /></td></tr></table>"
        return html
