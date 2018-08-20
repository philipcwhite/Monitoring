from django.shortcuts import render
from .models import AgentData, AgentEvent, AgentSystem, AgentThreshold, GlobalThreshold, Subscription

from .utils import mon_index, mon_device
from django.template.loader import render_to_string
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
    systemstatus = mon_device.system_status()
    context = {'systemstatus':systemstatus}
    return render(request, 'mon_app/devices.html', context)

def device(request, device_name):
    systemstatus = mon_device.system_status()
    context = {'systemstatus':systemstatus}
    return render(request, 'mon_app/device.html', context)

def device_content(request, device_name):
    context = {'systemstatus':systemstatus}
    return render(request, 'mon_app/device_content.html', context)