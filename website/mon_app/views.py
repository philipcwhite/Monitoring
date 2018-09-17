from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import AgentData, AgentEvent, AgentSystem, Subscription
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
    devicedata = mon_device.device_data(device_name)
    context = {'devicesystem':devicesystem,'devicedata':devicedata}
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

# Media_App Registration

def register(request):
    if request.method == 'POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            user=authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    else:
        form=UserCreationForm()
    return render(request, 'registration/register.html', {'form':form})


