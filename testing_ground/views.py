from django.shortcuts import render
from django.views import View
from .models import Reservation, Time, Room
from django.http import HttpResponse, JsonResponse
from django import forms
from .forms import MyForm
from django.core.cache import cache
import ast



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
        'selected_date': specific_date,
        'results': results,
    }

    html = render(request, template, context)
    return HttpResponse(html)


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
    specific_date = request.POST['selected_date']
    reservation = selectionArray(room_data, time_data)
    

    specific_times = Time.objects.all()
    room_list = Room.objects.all()

    results = dayView(room_list, specific_date, specific_times)

    context = {
        'choices': reservation,
        'results': results,
        'selected_date': specific_date
    }


    html = render(request, template, context)
    return HttpResponse(html)


def selectionArray(room, time):
    room_data = room
    time_data = time
    choice_array = []
    new_dict = {room_data: time_data}

    if new_dict not in choice_array:
        choice_array.append(new_dict)

    return choice_array


def MultiViewRes(request):
    template = "page2.html"
    room_data = request.POST['key']
    time_data = request.POST['value']
    specific_date = request.POST['selected_date']
    reservation = selectionArray(room_data, time_data)
    specific_times = Time.objects.all()
    room_list = Room.objects.all()
    results = dayView(room_list, specific_date, specific_times)



    if request.method == 'POST':
        context = {
            'choices': reservation,
            'results': results,
            'selected_date': specific_date,
        }
        return render(request, template, context)

    context = {
        'choices': reservation,
        'results': results,
        'selected_date': specific_date
    }


    html = render(request, template, context)
    return HttpResponse(html)


def MultiViewResList(request):
    template = "page2.html"
    room_data = request.POST['key']
    time_data = request.POST['value']
    specific_date = request.POST['selected_date']
    first_choice = request.POST['chosen_rooms']
    array_first_choice = ast.literal_eval(first_choice)
    reservation = selectionArray(room_data, time_data)
    specific_times = Time.objects.all()
    room_list = Room.objects.all()
    results = dayView(room_list, specific_date, specific_times)



    if request.method == 'POST':
        combined_list = ChosenRoomArray(reservation, array_first_choice)
        context = {
            'choices': reservation,
            'results': results,
            'selected_date': specific_date,
            'new_list': first_choice,
            'combined_list': combined_list,
        }
        return render(request, template, context)

    context = {
        'choices': reservation,
        'results': results,
        'selected_date': specific_date
    }


    html = render(request, template, context)
    return HttpResponse(html)

def ChosenRoomArray(new_choice, list):
    combo_list = list
    if not any(d == new_choice for d in combo_list):
        combo_list.append(new_choice)

    return combo_list


# def multiReservation(request):
#     template = "page3.html"
#     specific_times = Time.objects.all()
#     room_list = Room.objects.all()

#     room_data = request.POST['key']
#     time_data = request.POST['value']
#     specific_date = request.POST['selected_date']
    
#     new_choice = selectionArray(room_data, time_data)

#     update_list = cacheArray(new_choice)
#     reservation_list = cache.get('collected_game_array')
   

#     results = dayView(room_list, specific_date, specific_times)

#     context = {
#         'new_choice': new_choice,
#         'update_list': reservation_list,
#         'results': results,
#         'selected_date': specific_date
#     }

#     print(reservation_list)
#     html = render(request, template, context)
#     return HttpResponse(html)

def Page1(request):
    template = "page1.html"
    specific_date = '2023-05-07'
    specific_times = Time.objects.all()
    room_list = Room.objects.all()

    results = dayView(room_list, specific_date, specific_times)
    choices = []

    context = {
        'selected_date': specific_date,
        'results': results,
        'choices': choices
    }

    return render(request, template, context)


def Page2(request):
    template = 'page2.html'
    selected_room = request.POST['key']
    selected_time = request.POST['value']
    specific_date = request.POST['selected_date']
    choice_list = request.POST['choices']
    array_choice = ReturnArray(choice_list)
    specific_times = Time.objects.all()
    room_list = Room.objects.all()

    results = dayView(room_list, specific_date, specific_times)

    reservation = selectionArray(selected_room, selected_time)

    if request.method == 'POST':
        if select_counter <= 4:
            if not any(d == reservation for d in array_choice):
                array_choice.append(reservation)
                select_counter += 1
                
        context = {
            'reservation': reservation,
            'choices': array_choice,
            'results': results,
            'specific_date': specific_date
    }

        return render(request, template, context)

    context = {
        'reservation': reservation,
        'choices': array_choice,
        'results': results,
        'specific_date': specific_date
    }
  

    html = render(request, template, context)
    return HttpResponse(html)

def SelectedRoomList(list):
    combo_list = list
    if not any(d == new_choice for d in combo_list):
        combo_list.append(new_choice)

    return combo_list

def ReturnArray(input):
    new_input = input
    result = ast.literal_eval(new_input)

    return result
