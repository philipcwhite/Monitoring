#from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name='mon_app'
urlpatterns=[
    #Monitoring Application
    path('', views.index, name='index'),
    path('devices', views.devices, name='devices'),
    path('card', views.card, name='card'),
    path('index_content', views.index_content, name='index_content'),
]   

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
