from django import forms
from .validation import person_id_validator, name_validator


class getIDForm(forms.Form):
    sname = forms.CharField(max_length=100, validators=[name_validator])
    sid = forms.CharField(max_length=100, validators=[person_id_validator])


class getDormForm(forms.Form):
    sname = forms.CharField(max_length=100, validators=[name_validator])
    sid = forms.CharField(max_length=100, validators=[person_id_validator])
