import time, datetime, socket
from .models import AgentSystem, AgentEvent, AgentData
from django.conf import settings
from django.utils import timezone


class mon_index:
    def donut_avail():
        ok = 0
        down = 0
        total = ok + down
        uptime_check = 600
        currenttime = time.time()
        agentsystem = AgentSystem.objects.all().order_by('name')

        for i in agentsystem:
            if (i.timestamp + uptime_check) >= currenttime:
                ok += 1
            else:
                down += 1
        total = ok + down

        ok_perc = (ok / total) * 100
        down_perc = (down / total) * 100
        total_perc = str(ok_perc) + ' ' + str(down_perc)

        html = """<table style="width:100%"><tr><td style="width:50%;text-align:center">
        <svg width="130" height="130" viewBox="0 0 42 42" class="donut">
        <circle class="donut-ring" cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#d9534f" stroke-width="4"></circle>
        <circle class="donut-segment" cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#93C54B" stroke-width="4" stroke-dasharray='""" + total_perc +"""' stroke-dashoffset="25"></circle>
        </svg></td>
        <td style="width:50%"><b>Host Availability</b><br /><svg width="10" height="10"><rect width="10" height="10" style="fill:#93C54B" /></svg> """ + str(ok) + """ Hosts Up<br />
        <svg width="10" height="10"><rect width="10" height="10" style="fill:#d9534f" /></svg> """ + str(down) + """ Hosts Down</td></tr></table>"""

        return html

    def donut_alerts():
        info = 0
        warn = 0
        majr = 0
        crit = 0

        info = AgentEvent.objects.filter(status = 1, severity='Information').count()
        warn = AgentEvent.objects.filter(status = 1, severity='Warning').count()
        majr = AgentEvent.objects.filter(status = 1, severity='Major').count()
        crit = AgentEvent.objects.filter(status = 1, severity='Critical').count()

        total = info + warn + majr + crit
        if total == 0:
            total = 1
        info_perc = (info / total) * 100
        warn_perc = (warn / total) * 100
        majr_perc = (majr / total) * 100
        crit_perc = (crit / total) * 100
        info_points = str(info_perc) + ' ' + str(100 - info_perc)
        warn_points = str(warn_perc) + ' ' + str(100 - warn_perc)
        majr_points = str(majr_perc) + ' ' + str(100 - majr_perc)
        crit_points = str(crit_perc) + ' ' + str(100 - crit_perc)

        html = """<table style="width:100%"><tr><td style="width:50%;text-align:center">
        <svg width="130" height="130" viewBox="0 0 42 42" class="donut">
        <circle class="donut-ring" cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#93C54B" stroke-width="4"></circle>
        <circle class="donut-segment" cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#29ABE0" stroke-width="4" stroke-dasharray='""" + info_points +"""' stroke-dashoffset="25"></circle>
        <circle class="donut-segment" cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#ffc107" stroke-width="4" stroke-dasharray='""" + warn_points +"""' stroke-dashoffset='""" + str(100 - info_perc + 25) + """'></circle>
        <circle class="donut-segment" cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#F47C3C" stroke-width="4" stroke-dasharray='""" + majr_points +"""' stroke-dashoffset='""" + str(100 - info_perc - warn_perc + 25) + """'></circle>
        <circle class="donut-segment" cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#d9534f" stroke-width="4" stroke-dasharray='""" + crit_points +"""' stroke-dashoffset='""" + str(100 - info_perc - warn_perc - majr_perc + 25) + """'></circle>
        </svg></td><td style="width:50%"><b>Open Events</b><br />
        <svg width="10" height="10"><rect width="10" height="10" style="fill:#29ABE0" /></svg> """ + str(info) + """ Information<br />
        <svg width="10" height="10"><rect width="10" height="10" style="fill:#ffc107" /></svg> """ + str(warn) + """ Warning<br />
        <svg width="10" height="10"><rect width="10" height="10" style="fill:#F47C3C" /></svg> """ + str(majr) + """ Major<br />
        <svg width="10" height="10"><rect width="10" height="10" style="fill:#d9534f" /></svg> """ + str(crit) + """ Critical
        </td></tr></table>"""

        return html

    def system_perf():
        name = socket.gethostname().lower()
        agentsystem = AgentSystem.objects.get(name=name)
        uptime_check = 600
        currenttime = time.time()

        os = ""
        if 'Windows' in agentsystem.osname:
            os = 'Windows'
        elif 'Linux' in agentsystem.osname:
            os = 'Linux'

        agent_cpu_query = AgentData.objects.filter(name = name, monitor = 'perf.processor.percent.used').order_by('-id')[0]
        cpu_perc = agent_cpu_query.value
        agent_mem_query = AgentData.objects.filter(name = name, monitor = 'perf.memory.percent.used').order_by('-id')[0]
        mem_perc = agent_mem_query.value
        agent_timestamp = AgentSystem.objects.filter(name = name)[0].timestamp


        html = """<table style="width:100%;height:138px"><tr><td style="width:50%;padding-left:25px;padding-top:25px;vertical-align: text-top">
        <b>Monitoring Server</b><br />
        Name: """ + name + """<br />
        Processors: """ + str(agentsystem.processors + 1) + """<br />
        Memory: """ + str(agentsystem.memory)[:-3] + """ MB <br />
        OS: """ + os + """ (""" + agentsystem.osarchitecture + """) <br />
        </td><td style="width:50%;padding-left:10px;padding-top:25px;vertical-align: text-top"><b>Performance</b><br />"""

        if (agent_timestamp + uptime_check) >= currenttime:
            if cpu_perc >= 90:
                html = html + """<svg width="10" height="10"><rect width="10" height="10" style="fill:#d9534f" /></svg> """ + str(cpu_perc)[:-3] + """% CPU<br />"""
            else:
                html = html + """<svg width="10" height="10"><rect width="10" height="10" style="fill:#93C54B" /></svg> """ + str(cpu_perc)[:-3] + """% CPU<br />"""
            if mem_perc >= 90:
                html = html + """<svg width="10" height="10"><rect width="10" height="10" style="fill:#d9534f" /></svg> """ + str(mem_perc)[:-3] + """% Memory<br />"""
            else:
                html = html + """<svg width="10" height="10"><rect width="10" height="10" style="fill:#93C54B" /></svg> """ + str(mem_perc)[:-3] + """% Memory<br />"""
        else:
            html = html + "Agent Not Reporting"
        html = html + "</td></tr></table>"

        return html
 

    def system_status():
        agentsystem = AgentSystem.objects.all().order_by('name')
        uptime_check = 600
        currenttime = time.time()
        os = ""
        html = ""
        icon = ""

        for i in agentsystem:
            dt = datetime.datetime.fromtimestamp(i.timestamp)
            date = 'Last Reported: ' + str(timezone.make_aware(dt, timezone.utc)).replace(':00+00:00','')
            if 'Windows' in i.osname:
                os = 'Windows'
            elif 'Linux' in i.osname:
                os = 'Linux'

            if (i.timestamp + uptime_check) >= currenttime:
                icon = """<svg width="10" height="10"><rect width="10" height="10" style="fill:#93C54B" /></svg>"""
            else:
                icon =  """<svg width="10" height="10"><rect width="10" height="10" style="fill:#d9534f" /></svg>"""
                
            html = html + "<tr><td style='padding-left:20px'>" + icon + " &nbsp;<a href='device/" + str(i.name) + "'>" + str(i.name) + "</a></td><td>IP Address: " + str(i.ipaddress) + "</td><td>Domain: " + str(i.domain).lower() + "</td><td>Platform: " + os + " (" + str(i.osarchitecture) + ")</td><td>" + date + "</td></tr>"


        return html
