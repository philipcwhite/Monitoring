from django.shortcuts import render
from .models import AgentData, AgentEvent, AgentSystem, AgentThreshold, GlobalThreshold, Subscription
from .mon_device import mon_device, mon_devices
from .mon_index import mon_index
from .mon_events import mon_events


# Create your views here.

# Index main
def index(request):
    return render(request, 'mon_app/index.html')

def index_content(request):
    grapha = mon_index.donut_avail()
    graphb = mon_index.donut_alerts()
    systemperf = mon_index.system_perf()
    systemstatus = mon_index.system_status()
    context = {'grapha':grapha,'graphb':graphb,'systemperf':systemperf,'systemstatus':systemstatus}
    return render(request, 'mon_app/index_content.html', context)

# Devices
def devices(request):
    systemstatus = mon_devices.system_status()
    context = {'systemstatus':systemstatus}
    return render(request, 'mon_app/devices.html', context)

def device(request, device_name):
    devicename = device_name
    context = {'devicename':devicename}
    return render(request, 'mon_app/device.html', context)

def device_content(request, device_name):
    devicesystem = mon_device.device_system(device_name)
    devicegraph = mon_device.device_graph(device_name)
    context = {'devicesystem':devicesystem,'devicegraph':devicegraph}
    return render(request, 'mon_app/device_content.html', context)

def events(request):
    return render(request, 'mon_app/events.html')

def events_content(request):
    eventsummary = mon_events.event_summary()
    eventlist = mon_events.event_list()
    context = {'eventsummary':eventsummary,'eventlist':eventlist}
    return render(request, 'mon_app/events_content.html',context)

def event_close(request, event_id):
    eventclose = mon_events.event_close(event_id)
    return render(request, 'mon_app/events.html')

def reports(request):
    return render(request, 'mon_app/reports.html')

def settings(request):
    return render(request, 'mon_app/settings.html')
