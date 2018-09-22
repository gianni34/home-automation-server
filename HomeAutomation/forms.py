from django import forms
from HomeAutomation.models import *


class IntermediaryForm(forms.ModelForm):
    class Meta:
        model = Intermediary
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput(),
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput(),
        }
