
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput())

class AddStudentForm(forms.Form):
    name = forms.CharField(max_length=120)
    subject = forms.CharField(max_length=120)
    marks = forms.IntegerField(min_value=0, max_value=100)
