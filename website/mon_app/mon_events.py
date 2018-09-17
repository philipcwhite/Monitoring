import time, datetime, socket
from .models import AgentEvent
from django.conf import settings
from django.utils import timezone


class mon_events:

    def event_summary():
        total = 0
        info = 0
        warn = 0
        majr = 0
        crit = 0

        info = AgentEvent.objects.filter(status = 1, severity='4').count()
        warn = AgentEvent.objects.filter(status = 1, severity='3').count()
        majr = AgentEvent.objects.filter(status = 1, severity='2').count()
        crit = AgentEvent.objects.filter(status = 1, severity='1').count()

        total = info + warn + majr + crit

        html = """<table style="width:100%;text-align:center"><tr>
        <td style="text-align:left; padding-left:10px">Open Events</td>
        <td><svg width="10" height="10"><rect width="10" height="10" style="fill:#CCCCCC" /></svg>&nbsp; """ + str(total) + """&nbsp;  Total</td>
        <td><svg width="10" height="10"><rect width="10" height="10" style="fill:#29ABE0" /></svg>&nbsp;  """ + str(info) + """&nbsp;  Information</td>
        <td><svg width="10" height="10"><rect width="10" height="10" style="fill:#FFC107" /></svg>&nbsp;  """ + str(warn) + """&nbsp;  Warning</td>
        <td><svg width="10" height="10"><rect width="10" height="10" style="fill:#F47C3C" /></svg>&nbsp;  """ + str(majr) + """&nbsp;  Major</td>
        <td><svg width="10" height="10"><rect width="10" height="10" style="fill:#D9534F" /></svg>&nbsp;  """ + str(crit) + """&nbsp;  Critical</td>
        </tr></table>"""

        return html

    def event_list():

        agentevents = AgentEvent.objects.filter(status = 1).order_by('-timestamp')
        html = """<table style="width:100%">"""
        color = "#CCCCCC"

        for i in agentevents:
            dt = datetime.datetime.fromtimestamp(i.timestamp)
            date = str(timezone.make_aware(dt, timezone.utc)).replace(':00+00:00','')
            sev_text = ""
            if i.severity == "4":
                color = "#29ABE0"
                sev_text = "Information"
            elif i.severity == "3":
                color = "#FFC107"
                sev_text = "Warning"
            elif i.severity == "2":
                color = "#F47C3C"
                sev_text = "Major"
            elif i.severity == "1":
                color = "#D9534F"
                sev_text = "Critical"
            #i.eventdate.strftime("%Y-%m-%d %H:%M:%S")
            html = html + """<tr><td style="text-align:left;padding-left:10px">""" + date + """</td>
            <td style="text-align:left"><svg width="10" height="10"><rect width="10" height="10" style="fill:""" + color + """" /></svg> """ + sev_text + """</td>
            <td><a href="/device/""" + i.name + """">""" + i.name + """</a></td>
            <td>""" + i.message + """</td>
            <td style="text-align:right;padding-right:10px"><form><input type="button" onclick="window.location.href='/event_close/""" + str(i.id) + """'" class="action-button" value="Close Event" /></form></td>
            </tr>"""

            html = html + "</table"

        return html

    def event_close(event_id):
        agentevent = AgentEvent.objects.get(id = event_id)
        agentevent.status = False
        agentevent.save()

    
    