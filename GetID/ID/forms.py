from django import forms
from .front_validation import person_id_validator


class getIDForm(forms.Form):
    sname = forms.CharField(max_length=100)
    sid = forms.CharField(max_length=100)


class getDormForm(forms.Form):
    sname = forms.CharField(max_length=100)
    sid = forms.CharField(max_length=100)
