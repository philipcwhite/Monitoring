from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import AgentData, AgentEvent, AgentSystem, NotifyRule
from .forms import NotifyRuleForm
from .mon_device import mon_device, mon_devices
from .mon_index import mon_index
from .mon_events import mon_events

# Create your views here.

# Index main
@login_required
def index(request):
    page=1
    context = {"page":page}
    return render(request, "mon_app/index.html", context)

@login_required
def index_page(request,page):
    if page is None:page = 1
    context = {"page":page}
    return render(request, "mon_app/index.html", context)

@login_required
def index_content(request,page):
    grapha = mon_index.donut_avail()
    graphb = mon_index.donut_alerts()
    systemperf = mon_index.system_perf()
    systemstatus = mon_index.system_status(page)
    systemstatuspager = mon_index.system_status_pager(page)
    context = {"grapha":grapha,"graphb":graphb,"systemperf":systemperf,"systemstatus":systemstatus,"systemstatuspager":systemstatuspager}
    return render(request, "mon_app/index_content.html", context)

# Devices
@login_required
def devices(request):
    systemstatus = mon_devices.system_status()
    context = {"systemstatus":systemstatus}
    return render(request, "mon_app/devices.html", context)

@login_required
def device(request, device_name):
    devicename = device_name
    context = {"devicename":devicename}
    return render(request, "mon_app/device.html", context)

@login_required
def device_content(request, device_name):
    devicesystem = mon_device.device_system(device_name)
    devicedata = mon_device.device_data(device_name)
    context = {"devicesystem":devicesystem,"devicedata":devicedata}
    return render(request, "mon_app/device_content.html", context)

@login_required
def device_graph(request, device_name, monitor_name):
    devicename = device_name
    monitorname = monitor_name
    context = {"devicename":devicename, "monitorname":monitorname}
    return render(request, "mon_app/device_graph.html", context)

@login_required
def device_graph_content(request, device_name, monitor_name):
    devicename = device_name
    monitorname = monitor_name
    devicegraph = mon_device.device_graph(device_name, monitor_name)
    context = {"devicename":devicename, "monitorname":monitorname, "devicegraph":devicegraph}
    return render(request, "mon_app/device_graph_content.html", context)

# Events
@login_required
def events(request):
    return render(request, "mon_app/events.html")

@login_required
def events_content(request):
    eventsummary = mon_events.event_summary()
    eventlist = mon_events.event_list()
    context = {"eventsummary":eventsummary,"eventlist":eventlist}
    return render(request, "mon_app/events_content.html",context)

@login_required
def event_close(request, event_id):
    eventclose = mon_events.event_close(event_id)
    return render(request, "mon_app/events.html")

# Reports
@login_required
def reports(request):
    return render(request, "mon_app/reports.html")

# Settings
@login_required
def settings(request):
    return render(request, "mon_app/settings.html")

@login_required
def notify(request):
    notifyrule = NotifyRule.objects.all().order_by('notify_name')
    context = {"notifyrule":notifyrule}
    return render(request, "mon_app/notify.html", context)

@login_required
def notify_add(request):
    if request.method != 'POST':
        form=NotifyRuleForm()
    else:
        form = NotifyRuleForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('mon_app:settings'))
    return render(request, 'mon_app/notify_modify.html', {'form': form})

@login_required
def notify_edit(request, notify_id):
    notifyrule=NotifyRule.objects.get(id=notify_id)
    if request.method != 'POST':
        form=NotifyRuleForm(instance=notifyrule)
    else:
        form = NotifyRuleForm(instance=notifyrule, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('mon_app:settings'))
    context={'form':form}
    return render(request, 'mon_app/notify_modify.html', context)

@login_required
def notify_delete(request, notify_id):
    if request.method != 'POST':
        notifyrule=NotifyRule.objects.get(id=notify_id)
    else:
        notifyrule = get_object_or_404(NotifyRule, id=notify_id)
        notifyrule.delete()
        return HttpResponseRedirect(reverse('mon_app:settings'))
    context={'notifyrule':notifyrule}
    return render(request, 'mon_app/notify_modify.html', context)

# Search
@login_required
def search(request):
    query_string = ""
    found_entries = None
    if ("q" in request.GET) and request.GET["q"].strip():
        query_string = request.GET["q"]
        agents = AgentSystem.objects.filter(name__contains=query_string)
        return render(request, "mon_app/search.html", { "query_string": query_string, "agents": agents })
    else:
        return render(request, "mon_app/search.html", { "query_string": "Null" })


# Media_App Registration
def register(request):
    if request.method == "POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data["username"]
            password=form.cleaned_data["password1"]
            user=authenticate(username=username, password=password)
            login(request, user)
            return redirect("/")
    else:
        form=UserCreationForm()
    return render(request, "registration/register.html", {"form":form})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {'form': form})







