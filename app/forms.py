from django import forms

class locForm(forms.Form):
    Location = forms.CharField(widget=forms.TextInput(attrs={'class': 'formTextbox', 'id': 'loc'}), initial="")
    Distance = forms.CharField(widget=forms.TextInput(attrs={'class': 'formTextbox'}))