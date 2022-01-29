from django import forms

class locForm(forms.Form):
    Location = forms.CharField()
    Distance = forms.CharField()