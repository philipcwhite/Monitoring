#from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name='mon_app'
urlpatterns=[
    #Monitoring Application
    path('', views.index, name='index'),
    path('index_content', views.index_content, name='index_content'),
    path('devices', views.devices, name='devices'),
    path('device/<str:device_name>', views.device, name='device'),
    path('device_content/<str:device_name>', views.device_content, name='device_content'),
    path('events', views.events, name='events'),
    path('events_content', views.events_content, name='events_content'),
    path('event_close/<int:event_id>', views.event_close, name='event_close'),
    path('reports', views.reports, name='reports'),
    path('settings', views.settings, name='settings'),
    path('settings/thresholds/global', views.settings_global_thresholds, name='settings_global_thresholds'),
    path('settings/thresholds/global/add', views.settings_global_threshold_add, name='settings_global_threshold_add'),
    path('settings/thresholds/global/edit/<int:thresh_id>', views.settings_global_threshold_edit, name='settings_global_threshold_edit'),
    path('settings/thresholds/agent/<str:device_name>/add', views.settings_agent_threshold_add, name='settings_agent_threshold_add'),
    path('settings/thresholds/agent/edit/<int:thresh_id>', views.settings_agent_threshold_edit, name='settings_agent_threshold_edit'),
]   

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
