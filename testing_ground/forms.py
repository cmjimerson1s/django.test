from django import forms


class MyForm(forms.Form):
    key = forms.HiddenInput()
    value = forms.HiddenInput()
    selected_date = forms.HiddenInput()
    choices = forms.HiddenInput()
    selected_room_list = forms.HiddenInput()