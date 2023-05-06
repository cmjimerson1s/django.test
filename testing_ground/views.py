from django.shortcuts import render
from .models import Reservation, Time, Room
from django.http import HttpResponse, JsonResponse
from django import forms
from .forms import MyForm


# Create your views here.


def pageView(request):
    name = "Chris"
    template = "page1.html"
    context = {
        'name': name,
    }
    return render(request, template, context)

def resView(request):
    specific_date = "2023-05-07"
    specific_time = "14:00"
    template = 'page1.html'
    collected_data = {}
    keys = ["Horror", "Pirate"]

    values = [
        "12:00", "14:00", "16:00", "18:00"
    ]

    pairs = {key: values for key in keys}
    reservations = Reservation.objects.filter(date=specific_date, time=specific_time)


    # status = add_values_in_dict(collected_data, game, times)

    context = {
        'pairs': pairs, 
        'resevations': reservations,
    }

    return render(request, template, context)


def add_values_in_dict(sample_dict, key, list_of_values):
    ''' Append multiple values to a key in 
        the given dictionary '''
    if key not in sample_dict:
        sample_dict[key] = list()
    sample_dict[key].extend(list_of_values)
    result = dict(sample_dict)
    return result


def resultView(request):
    form = MyForm()
    template = "page1.html"
    specific_date = '2023-05-07'
    specific_times = Time.objects.all()
    room_list = Room.objects.all()

    results = dayView(room_list, specific_date, specific_times)

    context = {
        'results': results,
    }
    return render(request, template, context)


def checkRes(room, date, time):

    if (Reservation.objects.filter(date=date, room=room, time=time).exists()):
        result = 45
        return result
    else:
        result = time
        return result

def timeChecks(room, date, times):
    result = []
    for time in times:
        checked = checkRes(room, date, time)
        result.append(checked)
    return result

def dayView(rooms, date, times):
    result = []
    for room in rooms:
        time_list = timeChecks(room, date, times)
        list_pairs = {room: time_list}
        result.append(list_pairs)
    return result

def checkedBox(request):
    template = "page2.html"
    selected_game = request.POST['selection']


class MyForm(forms.Form):
    key = forms.CharField()
    value = forms.CharField()

def my_view(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            my_key = form.cleaned_data['key']
            my_value = form.cleaned_data['value']
            data = {
                'key': my_key,
                'value': my_value,
            }
            return JsonResponse(data)
    else:
        form = MyForm()
    return render(request, 'page1.html', {'form': form})


def choiceView(request):
    template = "page2.html"
    room_data = request.POST['key']
    time_data = request.POST['value']

    reservation_choice = selectionArray(room_data, time_data)

    specific_date = '2023-05-07'
    specific_times = Time.objects.all()
    room_list = Room.objects.all()

    results = dayView(room_list, specific_date, specific_times)

    context = {
        'choices': reservation_choice,
        'results': results
    }

    return render(request, template, context)


def selectionArray(room, time):
    room_data = room
    time_data = time
    new_dict = {room_data: time_data}

    choice_array = []

    if new_dict not in choice_array:
        choice_array.append(new_dict)

    return choice_array