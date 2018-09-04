from django.shortcuts import render
from .models import AgentData, AgentEvent, AgentSystem, AgentThreshold, GlobalThreshold, Subscription
from .forms import AgentThresholdForm, GlobalThresholdForm
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

# Events
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

# Reports
def reports(request):
    return render(request, 'mon_app/reports.html')

# Settings
def settings(request):
    return render(request, 'mon_app/settings.html')

def settings_global_thresholds(request):
    thresholds = GlobalThreshold.objects.all().order_by('monitor').order_by('severity')
    context = {'thresholds':thresholds}
    return render(request, 'mon_app/settings_thresholds_global.html', context)

def settings_global_threshold_add(request):
    if request.method != 'POST':
        form = GlobalThresholdForm()
    else:
        form = GlobalThresholdForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'mon_app/settings_thresholds_global.html')
    context = {'form': form}
    return render(request, 'mon_app/settings_thresholds_add.html', context)

def settings_global_threshold_edit(request, thresh_id):
    globalthreshold = GlobalThreshold.objects.get(id=thresh_id)
    if request.method != 'POST':
        form = GlobalThresholdForm(instance=globalthreshold)
    else:
        form = GlobalThresholdForm(instance=globalthreshold, data=request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'mon_app/settings_thresholds_global.html')
    context = {'form':form}
    return render(request, 'mon_app/settings_thresholds_edit.html', context)

def settings_global_threshold_delete(request):
    return render(request, 'mon_app/settings.html')

def settings_agent_thresholds(request, device_name):
    return render(request, 'mon_app/settings.html')

def settings_agent_threshold_add(request, device_name):
    name = device_name
    if request.method != 'POST':
        form = AgentThresholdForm()
    else:
        form = AgentThresholdForm(data = request.POST)
        if form.is_valid():
            athresh = form.save(commit = False)
            athresh.name = name
            athresh.save()
            return render(request, 'mon_app/settings.html')
    context = {'name':name,'form': form}
    return render(request, 'mon_app/settings_thresholds_add.html', context)

def settings_agent_threshold_edit(request, thresh_id):
    agentthreshold = AgentThreshold.objects.get(id=thresh_id)
    if request.method != 'POST':
        form = AgentThresholdForm(instance=agentthreshold)
    else:
        form = AgentThresholdForm(instance=agentthreshold, data=request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'mon_app/settings.html')
    context = {'form':form}
    return render(request, 'mon_app/settings_thresholds_edit.html', context)