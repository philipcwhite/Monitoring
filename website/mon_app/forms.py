from django import forms
from .models import AgentData, AgentThreshold, GlobalThreshold


class AgentDataForm(forms.ModelForm):
    class Meta:
        model = AgentData
        fields = ('timestamp','name', 'monitor', 'value', )

class AgentThresholdForm(forms.ModelForm):
    class Meta:
        model = AgentThreshold
        fields = ('monitor','severity', 'threshold', 'compare', 'timerange', 'enabled', )

class GlobalThresholdForm(forms.ModelForm):
    class Meta:
        model = GlobalThreshold
        fields = ('monitor','severity', 'threshold', 'compare', 'timerange', 'enabled', )

