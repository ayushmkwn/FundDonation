from django.contrib.auth.models import User
from django import forms


class forgotpwdForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]
        widgets = {
            'postname': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class resetpwdForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["password"]
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
