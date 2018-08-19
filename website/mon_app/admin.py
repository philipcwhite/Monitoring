from django.contrib import admin

# Register your models here.
from mon_app.models import AgentData, AgentEvent, AgentSystem, AgentThreshold, GlobalThreshold, Subscription

admin.site.register(AgentData)
admin.site.register(AgentEvent)
admin.site.register(AgentSystem)
admin.site.register(AgentThreshold)
admin.site.register(GlobalThreshold)
admin.site.register(Subscription)
