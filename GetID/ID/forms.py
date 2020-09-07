from django import forms
from ID.front_validation import person_id_validator


class getIDForm(forms.Form):
    sname = forms.CharField()
    sid = forms.CharField(validators=[person_id_validator])


class getDormForm(forms.Form):
    sname = forms.CharField()
    sid = forms.CharField()
