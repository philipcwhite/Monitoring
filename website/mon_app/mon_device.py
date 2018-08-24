import time, datetime, socket
from .models import AgentSystem, AgentEvent, AgentData
from django.conf import settings
from django.utils import timezone


class mon_device_graph:
    def __init__(self, time, pvalue, mvalue):
        self.time=time
        self.pvalue=pvalue
        self.mvalue=mvalue

class mon_device:
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

            html = html + "<tr><td>" + icon + "</td><td>" + str(i.name) + "</td><td>" + str(i.domain) + "</td><td>" + str(i.ipaddress) + "</td><td>" + str(i.osname) + "</td></tr>"

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

        for i in data_list:
            pvalue = str(round(100 - i.pvalue))
            mvalue = str(round(100 - i.mvalue))
            processor_polyline_data = processor_polyline_data + str(xvalue) + "," + pvalue + " "
            memory_polyline_data = memory_polyline_data + str(xvalue) + "," + mvalue + " "
            xvalue += 12 

        processor_polyline = '<polyline points="' + processor_polyline_data + '" style="fill:none;stroke:#29ABE0;stroke-width:2" />'
        memory_polyline = '<polyline points="' + memory_polyline_data + '" style="fill:none;stroke:#ffc107;stroke-width:2" />'


        
        ostring = ''
        for i in data_list:
            ostring = ostring + i.time + "|" + str(i.pvalue)  + "|" + str(i.mvalue) + ","

        


        html = """<svg height=120 width=725>
        <rect x=20 y=10 width=700 height=1 fill=#ddd />
        <rect x=20 y=35 width=700 height=1 fill=#ddd />
        <rect x=20 y=60 width=700 height=1 fill=#ddd />
        <rect x=20 y=85 width=700 height=1 fill=#ddd />
        <rect x=20 y=110 width=700 height=1 fill=#ddd />
        <rect x=25 y=10 width=1 height=100 fill=#ddd />
        <text x="0" y="15" fill="#000">100</text>
        <text x="5" y="40" fill="#000">75</text>
        <text x="5" y="65" fill="#000">50</text>
        <text x="5" y="90" fill="#000">25</text>
        <text x="10" y="115" fill="#000">0</text>
        """ + memory_polyline + processor_polyline + """

        </svg>""" + processor_polyline_data

        return html














