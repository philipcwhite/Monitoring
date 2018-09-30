from django import forms
from .models import AgentData, AgentSystem, NotifyRule


class AgentDataForm(forms.ModelForm):
    class Meta:
        model = AgentData
        fields = ('timestamp','name', 'monitor', 'value', )


class NotifyRuleForm(forms.ModelForm):
    class Meta:
        model = NotifyRule
        labels = {'notify_name':'Notify Name','notify_email':'Notify Email','agent_name':'Agent Name','agent_monitor':'Monitor','agent_severity':'Severity','agent_status':'Event Open','notify_enabled':'Enabled'}
        fields = ('notify_name','notify_email','agent_name','agent_monitor','agent_severity','agent_status','notify_enabled', )