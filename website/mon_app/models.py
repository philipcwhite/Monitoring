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
    CRIT = 'Critical'
    MAJR = 'Major'
    WARN = 'Warning'
    INFO = 'Information'
    severity_choices=(
        (CRIT, 'Critical'),
        (MAJR, 'Major'),
        (WARN, 'Warning'),
        (INFO, 'Information'),
    )
    id = models.BigAutoField(unique = True, primary_key = True)
    eventdate = models.DateTimeField(auto_now_add = True)
    name = models.CharField(max_length = 100)
    monitor = models.CharField(max_length = 250)
    message = models.CharField(max_length  = 250)
    status = models.BooleanField(default = True)
    severity = models.CharField(max_length = 11, choices = severity_choices, default = INFO)
    threshold = models.PositiveIntegerField()
    compare = models.CharField(max_length=2)
    timerange = models.PositiveIntegerField() 
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

class AgentThreshold(models.Model):
    CRIT = 'Critical'
    MAJR = 'Major'
    WARN = 'Warning'
    INFO = 'Information'
    severity_choices = (
        (CRIT, 'Critical'),
        (MAJR, 'Major'),
        (WARN, 'Warning'),
        (INFO, 'Information'),
    )
    GT = '>'
    GTEQ = '>='
    LT = '<'
    LTEQ = '<='
    EQ = '='
    NEQ = '!='
    compare_choices = (
        (GT, '>'),
        (GTEQ, '>='),
        (LT, '<'),
        (LTEQ, '<='),
        (EQ, '='),
        (NEQ, '!=')
    )
    id = models.AutoField(unique = True, primary_key = True)
    name = models.CharField(max_length = 100)
    monitor = models.CharField(max_length = 250)
    severity = models.CharField(max_length = 11, choices = severity_choices, default = INFO)
    threshold = models.PositiveIntegerField()
    compare = models.CharField(max_length=2, choices = compare_choices, default = GT)
    timerange = models.PositiveIntegerField() 
    enabled = models.BooleanField(default = True)
    class Meta:
        permissions = (('mon_admin','Monitoring Admin'),)
        verbose_name_plural = 'AgentThresholds'

class GlobalThreshold(models.Model):
    CRIT = 'Critical'
    MAJR = 'Major'
    WARN = 'Warning'
    INFO = 'Information'
    severity_choices=(
        (CRIT, 'Critical'),
        (MAJR, 'Major'),
        (WARN, 'Warning'),
        (INFO, 'Information'),
    )
    GT = '>'
    GTEQ = '>='
    LT = '<'
    LTEQ = '<='
    EQ = '='
    NEQ = '!='
    compare_choices = (
        (GT, '>'),
        (GTEQ, '>='),
        (LT, '<'),
        (LTEQ, '<='),
        (EQ, '='),
        (NEQ, '!=')
    )
    id = models.AutoField(unique = True, primary_key = True)
    monitor = models.CharField(max_length = 250)
    severity = models.CharField(max_length = 11, choices = severity_choices, default = INFO)
    threshold = models.PositiveIntegerField()
    compare = models.CharField(max_length=2, choices = compare_choices, default = GT)
    timerange = models.PositiveIntegerField() 
    enabled = models.BooleanField(default = True)
    class Meta:
        permissions = (('mon_admin','Monitoring Admin'),)
        verbose_name_plural = 'GlobalThresholds'

class Subscription(models.Model):
    id = models.AutoField(unique = True, primary_key = True)
    name = models.CharField(max_length = 100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notify = models.BooleanField(default = True)
    class Meta:
        permissions = (('mon_admin','Monitoring Admin'),)
        verbose_name_plural = 'Subscriptions'
