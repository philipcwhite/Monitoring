from django.contrib.auth import views as auth_views
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
    path('device/<str:device_name>/graph/<str:monitor_name>', views.device_graph, name='device_graph'),
    path('device_content/<str:device_name>/graph/<str:monitor_name>', views.device_graph_content, name='device_graph_content'),
    path('events', views.events, name='events'),
    path('events_content', views.events_content, name='events_content'),
    path('event_close/<int:event_id>', views.event_close, name='event_close'),
    path('reports', views.reports, name='reports'),
    path('settings', views.settings, name='settings'), 
    path('search', views.search, name='search'), 
    #User Management
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), {'next_page': '/'}, name='logout'),   
]   

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
