import time, datetime, socket
from .models import AgentSystem, AgentData
from django.conf import settings
from django.utils import timezone

class mon_device_graph:
    def __init__(self, time, pvalue, mvalue):
        self.time=time
        self.pvalue=pvalue
        self.mvalue=mvalue

class mon_device:
    
    def device_system(name):
        agentsystem = AgentSystem.objects.get(name=name)

        html="""<table style="width:100%"><tr>
        <td><b>Name:</b> """ + agentsystem.name + """</td>
        <td><b>IP Address:</b> """ + agentsystem.ipaddress + """</td>
        <td><b>Domain:</b> """ + agentsystem.domain.lower() + """</td>
        <td><b>Platform:</b> """ + agentsystem.osname + " (" + agentsystem.osarchitecture + """)</td>
        <td><b>Build:</b> """ + str(agentsystem.osbuild) + """</td>
        <td><b>Processors:</b> """ + str(agentsystem.processors + 1) + """</td>
        <td><b>Memory:</b> """ + str(agentsystem.memory)[:-3] + """ MB</td>
        </tr></table>"""

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
                uptime_days = round(i.value / 60 / 60 / 24, 0)
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
                        <td>""" + fs_name + """ drive</td>
                        <td>Free Space: """ + fs_free + """</td>
                        <td>Filesystem Activity: """ + fs_active + """</td>
                        </tr></table>"""
            except:
                pass
        html_fs += """</div></div></td></tr>"""

        html = r"""<tr>
            <td style="padding-right:4px;text-align:center">
            <div class="card-div" style="height:70px">
            <div class="card-header">Processor (% used)</div>
            <div style="font-size:40px;font-weight:bold;color:#29ABE0;height:50px;line-height:50px">""" + str(cpu_perc) + """</div>
            </div></td>
            <td style="padding-left:4px;padding-right:4px;text-align:center">
            <div class="card-div" style="height:70px">
            <div class="card-header">Memory (% used)</div>
            <span style="font-size:40px;font-weight:bold;color:#29ABE0;height:50px;line-height:50px">""" + str(mem_perc) + """</span>
            </div></td>
            <td style="padding-left:4px;padding-right:4px;text-align:center">
            <div class="card-div" style="height:70px">
            <div class="card-header">Pagefile (% used)</div>
            <span style="font-size:40px;font-weight:bold;color:#29ABE0;height:50px;line-height:50px">""" + str(pagefile_perc) + """</span>
            </div></td>
            <td style="padding-left:4px;text-align:center">
            <div class="card-div" style="height:70px">
            <div class="card-header">Uptime (days)</div>
            <span style="font-size:40px;font-weight:bold;color:#29ABE0;height:50px;line-height:50px">""" + str(uptime_days) + """</span>
            </div></td></tr></table>
            <table style="width:100%">  
            <tr><td style="padding-bottom:4px;text-align:left">
            <div class="card-div">
            <div class="card-header">Network Monitors</div>
            <div style="padding-left: 10px">
            <table style="width:100%"><tr>
            <td>Network Total Traffic</td>
            <td>Bytes Sent: """ + str(net_bs) + """</td>
            <td>Bytes Received: """ + str(net_br) + """</td>
            </tr></table></div></div>
            </td></tr>"""
        html += html_fs

        return html

    def device_graph(name):
        processor_data = AgentData.objects.filter(name = name, monitor = 'perf.processor.percent.used').order_by('-id')[:60]
        memory_data = AgentData.objects.filter(name = name, monitor = 'perf.memory.percent.used').order_by('-id')[:60]
        data_list = []
        graph_time = datetime.datetime.now() - datetime.timedelta(minutes=59)

        for i in range(60):
            agent_data = mon_device_graph(time=graph_time.strftime('%H:%M'),pvalue=0,mvalue=0)
            data_list.append(agent_data)
            graph_time = graph_time + datetime.timedelta(minutes=1)

        for i in processor_data:
            processor_value = i.value
            time_short = timezone.make_aware(datetime.datetime.fromtimestamp(i.timestamp), timezone.utc).strftime('%H:%M')
            for i in data_list:
                if i.time == time_short:
                    i.pvalue = processor_value
        
        for i in memory_data:
            memory_value = i.value
            time_short = timezone.make_aware(datetime.datetime.fromtimestamp(i.timestamp), timezone.utc).strftime('%H:%M')
            for i in data_list:
                if i.time == time_short:
                    i.mvalue = memory_value
        
        processor_polyline = ''
        processor_polyline_data = ''
        memory_polyline = ''
        memory_polyline_data = ''
        xvalue = 25
        x2 = 20

        for i in data_list:
            pvalue = str(round(110 - i.pvalue))
            mvalue = str(round(110 - i.mvalue))
            m2 = str(round(i.mvalue))
            processor_polyline_data += str(xvalue) + "," + pvalue + " "
            memory_polyline_data += str(xvalue) + "," + mvalue + " "
            xvalue += 14 

        processor_polyline = '<polyline points="' + processor_polyline_data + '" style="fill:none;stroke:#29ABE0;stroke-width:1" />'
        memory_polyline = '<polyline points="' + memory_polyline_data + '" style="fill:none;stroke:#ffc107;stroke-width:1" />'
        
            
        html =  """<svg xmlns="http://www.w3.org/2000/svg" style="color:#8E8C84;" height=120 width=990>
	    <rect x=20 y=10 width=835 height=1 fill=#ddd />
        <rect x=20 y=35 width=835 height=1 fill=#ddd />
        <rect x=20 y=60 width=835 height=1 fill=#ddd />
        <rect x=20 y=85 width=835 height=1 fill=#ddd />
        <rect x=20 y=110 width=835 height=1 fill=#ddd />
        <rect x=25 y=10 width=1 height=100 fill=#ddd />
        <text x="0" y="15" fill="#8E8C84">100</text>
        <text x="5" y="40" fill="#8E8C84">75</text>
        <text x="5" y="65" fill="#8E8C84">50</text>
        <text x="5" y="90" fill="#8E8C84">25</text>
        <text x="10" y="115" fill="#8E8C84">0</text>
        <rect x=885 y=40 width="10" height="10" style="fill:#29ABE0" />
        <rect x=885 y=60 width="10" height="10" style="fill:#ffc107" />
        <text x="905" y="50" fill="#8E8C84">processor (%)</text>
        <text x="905" y="70" fill="#8E8C84">memory (%)</text>
        """ + memory_polyline + processor_polyline + """
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
