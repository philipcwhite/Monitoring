from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class AgentData(models.Model):
    id = models.BigAutoField(unique = True, primary_key = True)
    timestamp = models.PositiveIntegerField()
    name = models.CharField(max_length = 100)
    monitor = models.CharField(max_length = 250)
    value = models.DecimalField(max_digits = 50, decimal_places = 2)
    class Meta:
        permissions = (('mon_admin','Monitoring Admin'),)
        verbose_name_plural = 'AgentData'
    def __str__(self):
        return self.name

class AgentEvent(models.Model):
    CRIT = '1'
    MAJR = '2'
    WARN = '3'
    INFO = '4'
    severity_choices=(
        (CRIT, 'Critical'),
        (MAJR, 'Major'),
        (WARN, 'Warning'),
        (INFO, 'Information'),
    )
    id = models.BigAutoField(unique = True, primary_key = True)
    timestamp = models.PositiveIntegerField()
    name = models.CharField(max_length = 100)
    monitor = models.CharField(max_length  = 250)
    message = models.CharField(max_length  = 250)
    status = models.BooleanField(default = True)
    severity = models.CharField(max_length = 11, choices = severity_choices, default = INFO)
    class Meta:
        permissions = (('mon_admin','Monitoring Admin'),)
        verbose_name_plural = 'AgentEvents'
    def __str__(self):
        return self.message

class AgentSystem(models.Model):
    id = models.AutoField(unique = True, primary_key = True)
    timestamp = models.PositiveIntegerField()
    name = models.CharField(max_length = 100)
    ipaddress = models.CharField(max_length = 100, null = True, blank = True)
    osname = models.CharField(max_length = 250, null = True, blank = True)
    osbuild = models.CharField(max_length = 50, null = True, blank = True)
    osarchitecture = models.CharField(max_length = 25, null = True, blank = True)
    domain = models.CharField(max_length = 100, null = True, blank = True)
    processors = models.PositiveIntegerField(null = True, blank = True)
    memory = models.DecimalField(max_digits = 10, decimal_places = 2, null = True, blank = True)
    class Meta:
        permissions = (('mon_admin','Monitoring Admin'),)
        verbose_name_plural = 'AgentSystem'
    def __str__(self):
        return self.name

class Subscription(models.Model):
    id = models.AutoField(unique = True, primary_key = True)
    name = models.CharField(max_length = 100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notify = models.BooleanField(default = True)
    class Meta:
        permissions = (('mon_admin','Monitoring Admin'),)
        verbose_name_plural = 'Subscriptions'
