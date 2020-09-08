from django import forms
from .front_validation import person_id_validator


class getIDForm(forms.Form):
    sname = forms.CharField()
    sid = forms.CharField()


class getDormForm(forms.Form):
    sname = forms.CharField()
    sid = forms.CharField()
