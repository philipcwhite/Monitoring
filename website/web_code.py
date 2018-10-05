import time, datetime, socket, math
from web_data import WebData
from web_views import WebViews

class WebIndex:
    def index_block_1():
        ok = 0
        down = 0
        total = ok + down
        uptime_check = 300
        currenttime = time.time()
        agentsystem = WebData.web_code_index_device_avail()
        for i in agentsystem:
            timestamp = int(i['timestamp'])
            if (timestamp + uptime_check) >= currenttime:
                ok += 1
            else:
                down += 1
        total = ok + down
        if total == 0:total = 1
        ok_perc = (ok / total) * 100
        down_perc = (down / total) * 100
        total_perc = str(ok_perc) + ' ' + str(down_perc)

        html = """<table style="width:100%;height:105px"><tr><td style="width:50%;text-align:center;">
        <svg width="95" height="95" viewBox="0 0 42 42" class="donut">
        <circle class="donut-ring" cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#d9534f" stroke-width="5"></circle>
        <circle class="donut-segment" cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#93C54B" stroke-width="5" stroke-dasharray='""" + total_perc +"""' stroke-dashoffset="25"></circle>
        </svg></td>
        <td style="width:50%;vertical-align:top;padding-top:34px"><svg width="10" height="10"><rect width="10" height="10" style="fill:#93C54B" /></svg> """ + str(ok) + """ Hosts Up<br />
        <svg width="10" height="10"><rect width="10" height="10" style="fill:#d9534f" /></svg> """ + str(down) + """ Hosts Down</td></tr></table>"""
        return html

    def index_block_2():
        info = 0
        warn = 0
        majr = 0
        crit = 0
        agentevents = WebData.web_code_event_totals()
        for i in agentevents:
            sev = int(i['severity'])
            sev_tot = int(i['total'])
            if sev == 1:
                crit = sev_tot
            elif sev == 2:
                majr = sev_tot
            elif sev == 3:
                warn = sev_tot
            elif sev == 4:
                info = sev_tot
        total = info + warn + majr + crit
        if total == 0:total = 1
        info_perc = (info / total) * 100
        warn_perc = (warn / total) * 100
        majr_perc = (majr / total) * 100
        crit_perc = (crit / total) * 100
        info_points = str(info_perc) + ' ' + str(100 - info_perc)
        warn_points = str(warn_perc) + ' ' + str(100 - warn_perc)
        majr_points = str(majr_perc) + ' ' + str(100 - majr_perc)
        crit_points = str(crit_perc) + ' ' + str(100 - crit_perc)
        html = """<table style="width:100%;height:105px"><tr><td style="width:50%;text-align:center">
        <svg width="95" height="95" viewBox="0 0 42 42" class="donut">
        <circle class="donut-ring" cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#93C54B" stroke-width="5"></circle>
        <circle class="donut-segment" cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#29ABE0" stroke-width="5" stroke-dasharray='""" + info_points +"""' stroke-dashoffset="25"></circle>
        <circle class="donut-segment" cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#ffc107" stroke-width="5" stroke-dasharray='""" + warn_points +"""' stroke-dashoffset='""" + str(100 - info_perc + 25) + """'></circle>
        <circle class="donut-segment" cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#F47C3C" stroke-width="5" stroke-dasharray='""" + majr_points +"""' stroke-dashoffset='""" + str(100 - info_perc - warn_perc + 25) + """'></circle>
        <circle class="donut-segment" cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#d9534f" stroke-width="5" stroke-dasharray='""" + crit_points +"""' stroke-dashoffset='""" + str(100 - info_perc - warn_perc - majr_perc + 25) + """'></circle>
        </svg></td><td style="width:50%;vertical-align:top;padding-top:16px">
        <svg width="10" height="10"><rect width="10" height="10" style="fill:#29ABE0" /></svg> """ + str(info) + """ Information<br />
        <svg width="10" height="10"><rect width="10" height="10" style="fill:#ffc107" /></svg> """ + str(warn) + """ Warning<br />
        <svg width="10" height="10"><rect width="10" height="10" style="fill:#F47C3C" /></svg> """ + str(majr) + """ Major<br />
        <svg width="10" height="10"><rect width="10" height="10" style="fill:#d9534f" /></svg> """ + str(crit) + """ Critical
        </td></tr></table>"""
        return html

    def index_block_3():
        name = socket.gethostname().lower()
        uptime_check = 300
        currenttime = time.time()
        agent_platform = ""
        agent_architecture = ""
        agent_timestamp = 0
        agent_processors = 0
        agent_memory = 0
        cpu_perc = 0
        mem_perc = 0
        try:
            agentsystem = WebData.web_code_device_system(name)
            agent_platform = agentsystem['platform']
            agent_architecture = agentsystem['architecture']
            agent_timestamp = agentsystem['timestamp']
            agent_processors = agentsystem['processors']
            agent_memory = agentsystem['memory']
        except:
            pass
        try:
            agent_cpu_query = WebData.web_code_device_data_latest(name, 'perf.processor.percent.used')
            cpu_perc = agent_cpu_query['value']
            agent_mem_query = WebData.web_code_device_data_latest(name, 'perf.memory.percent.used')
            mem_perc = agent_mem_query['value']
        except:
            pass
        html = """<table style="width:100%;height:105px"><tr><td style="width:50%;padding-left:25px;vertical-align:top;padding-top:10px">
        Name: """ + name + """<br />
        Processors: """ + str(agent_processors) + """<br />
        Memory: """ + str(agent_memory)[:-3] + """ MB <br />
        Platform: """ + agent_platform + """ (""" + agent_architecture + """) <br />
        </td><td style="width:50%;padding-left:10px;vertical-align:top;padding-top:10px">"""

        if (agent_timestamp + uptime_check) >= currenttime:
            cpu_color = "93C54B"
            mem_color = "93C54B"
            if cpu_perc >= 90 : cpu_color = "D9534F"
            html = html + """<svg width="10" height="10"><rect width="10" height="10" style="fill:#""" + cpu_color + """" /></svg> """ + str(cpu_perc)[:-3] + """% CPU<br />"""
            if mem_perc >= 90: mem_color = "D9534F"
            html = html + """<svg width="10" height="10"><rect width="10" height="10" style="fill:#""" + mem_color + """" /></svg> """ + str(mem_perc)[:-3] + """% Memory<br />"""
        else:
            html = html + "Agent Not Reporting"
        html = html + "</td></tr></table>"
        return html

    def index_block_4(page):
        page_start = (page * 100) - 100
        page_end = page_start + 100
        agentsystem = WebData.web_code_index_devices(page_start, page_end)
        uptime_check = 300
        currenttime = time.time()
        os = ""
        html = ""
        icon = ""
        for i in agentsystem:
            dt = datetime.datetime.fromtimestamp(int(i['timestamp']))
            date = """<span style="padding-right:10px">Last Reported: """ + str(dt) + "</span>"
            color = "93C54B"
            if (int(i['timestamp']) + uptime_check) < currenttime : color = "D9534F"
            icon = """<svg width="10" height="10"><rect width="10" height="10" style="fill:#""" + color + """" /></svg>"""
            html += "<tr><td style='padding-left:20px'>" + icon + " &nbsp;<a href='devices/" + str(i['name']) + "'>" + str(i['name']) + r"</a></td><td>IP Address: " + str(i['ipaddress']) + r"</td><td>Domain: " + str(i['domain']).lower() + r"</td><td>Platform: " + str(i['platform']) + r" (" + str(i['architecture']) + r")</td><td>" + date + r"</td></tr>"
        return html

    def index_block_pager(page):
        page_start = (page * 100) - 100
        page_end = page_start + 100
        agent_count = WebData.web_code_index_device_count()
        page_count = int(math.ceil(int(agent_count['total']) / 100))
        uptime_check = 300
        currenttime = time.time()
        html = ""
        icon = ""
        html = ""
        if page_count > 1:
            for i in range(1,page_count + 1):
                if i == page:
                    html += """<td style="width:10px">""" + str(i) + "</td>"
                elif i == 1:
                    html += """<td style="width:10px"><a href="/">""" + str(i) + """</a></td>"""
                else:
                    html += """<td style="width:10px"><a href="/""" + str(i) + """">""" + str(i) + """</a></td>"""
        return html

    def index_content(qstring="page=1"):
        html=""
        pstring=str(qstring)
        page = int(pstring.replace("page=", ""))
        html += WebViews.load_index_content(WebIndex.index_block_1(), WebIndex.index_block_2(), WebIndex.index_block_3(), WebIndex.index_block_4(page), WebIndex.index_block_pager(page))
        return html

class WebSearch:
    def search_devices(device):
        results = WebData.web_code_device_system_search(device)
        html = "Host names containing: " + str(device) + "<br />"
        for i in results:
            html += """<a href="/devices/""""" + str(i["name"]) + """/">""" + str(i["name"]) + "</a></br />"
        return html