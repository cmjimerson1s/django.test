from django.shortcuts import render
from .models import Reservation, Time, Room
from django.http import HttpResponse


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
        result = 501
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
