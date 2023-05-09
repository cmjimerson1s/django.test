from django import forms
from .models import Reservation, TestModel


class MyForm(forms.Form):
    key = forms.HiddenInput()
    value = forms.HiddenInput()
    selected_date = forms.HiddenInput()
    # choices = forms.HiddenInput()
    # selected_room_list = forms.HiddenInput()


class ResForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date', 'time', 'room']


class TestForm(forms.ModelForm):
    class Meta:
        model = TestModel
        fields = ['name', 'email']
        widget = {
            'date': forms.HiddenInput(),
            'room': forms.HiddenInput(),
            'time': forms.HiddenInput(),
        }


