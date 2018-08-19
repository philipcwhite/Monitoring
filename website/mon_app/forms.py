from django import forms
from .models import AgentData


class AgentDataForm(forms.ModelForm):
    class Meta:
        model = AgentData
        fields = ('timestamp','name', 'monitor', 'value', )