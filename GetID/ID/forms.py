from django import forms


class getIDForm(forms.Form):
    sname = forms.CharField()
    sid = forms.CharField()


class getDormForm(forms.Form):
    sname = forms.CharField()
    sid = forms.CharField()
