from django import forms

class getIDForm(forms.Form):
    sname=forms.CharField()
    sid=forms.CharField()

class getDoomForm(forms.Form):
    sname=forms.CharField()
    sid=forms.CharField()