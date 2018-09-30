import time, datetime, socket
from .models import AgentSystem, AgentData
from django.conf import settings
from django.utils import timezone

class mon_device_graph:
    def __init__(self, time, dvalue):
        self.time=time
        self.dvalue=dvalue


class mon_device:
    
    def device_system(name):
        agentsystem = AgentSystem.objects.get(name=name)

        html="""<table style="width:100%"><tr>
        <td><b>Name:</b> """ + agentsystem.name + """</td>
        <td><b>IP Address:</b> """ + agentsystem.ipaddress + """</td>
        <td><b>Domain:</b> """ + agentsystem.domain.lower() + """</td>
        <td><b>Platform:</b> """ + agentsystem.osname + " (" + agentsystem.osarchitecture + """)</td>
        <td><b>Build:</b> """ + str(agentsystem.osbuild) + """</td>
        <td><b>Processors:</b> """ + str(agentsystem.processors) + """</td>
        <td><b>Memory:</b> """ + str(agentsystem.memory)[:-3] + """ MB</td>
        </tr></table>"""

        """agentsystem2 = AgentSystem.objects.values('name').distinct()
        for i in agentsystem2:
            html += str(i['name'])"""

        return html


    def device_data(name):  
        agentsystem = AgentSystem.objects.get(name=name)
        agent_time_query = AgentData.objects.filter(name = name).order_by('-id')[0]
        agent_time = agent_time_query.timestamp
        agent_query = AgentData.objects.filter(name = name, timestamp = agent_time)

        cpu_perc = 0
        mem_perc = 0
        pagefile_perc = 0
        uptime_days = 0
        net_br = 0
        net_bs = 0
        fs_list = []
        for i in agent_query:
            if i.monitor == 'perf.processor.percent.used':
                cpu_perc = round(i.value, 0)
            if i.monitor == 'perf.memory.percent.used':
                mem_perc = round(i.value, 0)
            if i.monitor == 'perf.pagefile.percent.used':
                pagefile_perc = round(i.value, 0)
            if i.monitor == 'perf.system.uptime.seconds':
                uptime_days = round(i.value / 86400, 0)
            if i.monitor == 'perf.network.bytes.received':
                net_br = round(i.value, 0)
            if i.monitor == 'perf.network.bytes.sent':
                net_bs = round(i.value, 0)

            if 'filesystem' in i.monitor and 'active' in i.monitor:
                fs_name = i.monitor.replace('perf.filesystem.','').replace('.percent.active','')
                fs_list.append(fs_name)
        
        html_fs = """<tr>
                    <td  style="padding-bottom:4px;text-align:left">
                            <div class="card-div">
                                <div class="card-header">Filesystem Monitors</div>
                                <div style="padding-left: 10px">"""
        for i in fs_list:
            """fs_query_free = AgentData.objects.filter(name = name, timestamp = agent_time, monitor = 'perf.filesystem.c.percent.free')[0]
            html_fs += str(i)
            html_fs += str(fs_query_free.value)"""
            try:
                fs_query_free = AgentData.objects.filter(name = name, timestamp = agent_time, monitor = 'perf.filesystem.' + i + '.percent.free')[0]
                fs_query_active = AgentData.objects.filter(name = name, timestamp = agent_time, monitor = 'perf.filesystem.' + i + '.percent.active')[0]
                fs_free = str(round(fs_query_free.value,0))
                fs_active = str(round(fs_query_active.value,0))
                fs_name = ""
                if agentsystem.osname == 'Windows':
                    fs_name = "Windows " + i + " drive"
                elif agentsystem.osname == 'Linux':
                    fs_name = "Linux Filesystem: " + i             
                html_fs += """<table style="width:100%"><tr>
                        <td style="width:33%">""" + fs_name + """ drive</td>
                        <td style="width:33%"><a href="/device/""" + name + """/graph/perf.filesystem.""" + i + """.percent.free">Free Space: """ + fs_free + """</a></td>
                        <td style="width:33%"><a href="/device/""" + name + """/graph/perf.filesystem.""" + i + """.percent.active">Filesystem Activity: """ + fs_active + """</a></td>
                        </tr></table>"""
            except:
                pass
        html_fs += """</div></div></td></tr>"""

        html = """<tr><td style="padding-right:4px;text-align:center">
            <div class="card-div" style="height:70px">
            <div class="card-header">Processor (% used)</div>
            <div  class="device-stats"><a class="device-stats" href="/device/""" + name + """/graph/perf.processor.percent.used">""" + str(cpu_perc) + """</a></div>
            </div></td>
            <td style="padding-left:4px;padding-right:4px;text-align:center">
            <div class="card-div" style="height:70px">
            <div class="card-header">Memory (% used)</div>
            <span class="device-stats"><a class="device-stats" href="/device/""" + name + """/graph/perf.memory.percent.used">"""  + str(mem_perc) + """</a></span>
            </div></td>
            <td style="padding-left:4px;padding-right:4px;text-align:center">
            <div class="card-div" style="height:70px">
            <div class="card-header">Pagefile (% used)</div>
            <span class="device-stats"><a class="device-stats" href="/device/""" + name + """/graph/perf.pagefile.percent.used">"""  + str(pagefile_perc) + """</a></span>
            </div></td>
            <td style="padding-left:4px;text-align:center">
            <div class="card-div" style="height:70px">
            <div class="card-header">Uptime (days)</div>
            <span class="device-stats"><a class="device-stats" href="/device/""" + name + """/graph/perf.system.uptime.seconds">"""  + str(uptime_days) + """</a></span>
            </div></td></tr></table>
            <table style="width:100%">  
            <tr><td style="padding-bottom:4px;text-align:left">
            <div class="card-div">
            <div class="card-header">Network Monitors</div>
            <div style="padding-left: 10px">
            <table style="width:100%"><tr>
            <td style="width:33%">Network Total Traffic</td>
            <td style="width:33%"><a href="/device/""" + name + """/graph/perf.network.bytes.sent">Bytes Sent: """ + str(net_bs) + """</a></td>
            <td style="width:33%"><a href="/device/""" + name + """/graph/perf.network.bytes.received">Bytes Received: """ + str(net_br) + """</a></td>
            </tr></table></div></div></td></tr>"""
        html += html_fs

        return html

    def device_graph(name, monitor):
        device_data = AgentData.objects.filter(name = name, monitor = monitor).order_by('-id')[:61]
        data_list = []
        max_value = 0
        mid_value = 0
        graph_time = datetime.datetime.now() - datetime.timedelta(minutes=60)

        for i in range(61):
            agent_data = mon_device_graph(time=graph_time.strftime('%H:%M'),dvalue=0)
            data_list.append(agent_data)
            graph_time = graph_time + datetime.timedelta(minutes=1)

        for i in device_data:
            if i.value > max_value:max_value = i.value
            
        for i in device_data:
            device_value = i.value
            time_short = timezone.make_aware(datetime.datetime.fromtimestamp(i.timestamp), timezone.utc).strftime('%H:%M')
            for i in data_list:
                if i.time == time_short:
                    if device_value == 0:
                        i.dvalue = 0
                    else:
                        i.dvalue = (device_value / max_value)*100


        

        device_polyline = ""
        device_polyline_data = ""
        device_time = ""
        xvalue = 55
        time_x = 0

        for i in data_list:
            dvalue = str(round(110 - i.dvalue))
            device_polyline_data += str(xvalue) + "," + dvalue + " "
            time_x += 1
            if time_x == 1:
                device_time += """<text x='""" + str(xvalue) + """' y="130" fill="#8E8C84" text-anchor="middle">""" + str(i.time) + """</text>"""
            if time_x == 5:
                time_x = 0
            
            
            
            
                

        

            xvalue += 14 
        device_polyline = '<polyline points="' + device_polyline_data + '" style="fill:none;stroke:#29ABE0;stroke-width:1" />'
                
        html =  """<svg xmlns="http://www.w3.org/2000/svg" style="color:#8E8C84;" height=150 width=990>
	    <rect x=52 y=10 width=855 height=1 fill=#ddd />
        <rect x=55 y=35 width=855 height=1 fill=#ddd />
        <rect x=52 y=60 width=855 height=1 fill=#ddd />
        <rect x=55 y=85 width=855 height=1 fill=#ddd />
        <rect x=52 y=110 width=855 height=1 fill=#ddd />
        <rect x=55 y=10 width=1 height=100 fill=#ddd />
        <text x="47" y="15" fill="#8E8C84" text-anchor="end">""" + str(int(max_value)) + """</text>
        <text x="47" y="65" fill="#8E8C84" text-anchor="end">""" + str(int(max_value / 2)) + """</text>
        <text x="47" y="115" fill="#8E8C84" text-anchor="end">0</text>
        """ + device_polyline + device_time + """
		</svg>""" 

        return html


class mon_devices:
    def system_status():
        agentsystem = AgentSystem.objects.all().order_by('name')
        uptime_check = 600
        currenttime = time.time()
        html = ""
        icon = ""

        for i in agentsystem:
            if (i.timestamp + uptime_check) >= currenttime:
                icon = """<svg width="10" height="10"><rect width="10" height="10" style="fill:#93C54B" /></svg>"""
            else:
                icon =  """<svg width="10" height="10"><rect width="10" height="10" style="fill:#d9534f" /></svg>"""

            html = html + """<tr><td style="padding-left:10px">""" + icon + "</td><td><a href='/device/" + str(i.name) + "'>" + str(i.name) + "</td><td>" + str(i.domain) + "</td><td>" + str(i.ipaddress) + "</td><td>" + str(i.osname) + "</td></tr>"

        return html
