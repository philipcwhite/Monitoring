from django.contrib import admin

# Register your models here.
from mon_app.models import AgentData, AgentEvent, AgentSystem, Subscription

admin.site.register(AgentData)
admin.site.register(AgentEvent)
admin.site.register(AgentSystem)
admin.site.register(Subscription)
