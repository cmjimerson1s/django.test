from django import forms


class MyForm(forms.Form):
    key = forms.HiddenInput()
    value = forms.HiddenInput()