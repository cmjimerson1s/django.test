from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import FormView
from .models import Reservation, Time, Room, TestModel
from django.http import HttpResponse, JsonResponse
from django import forms
from .forms import MyForm, ResForm, TestForm
from django.core.cache import cache
import ast
import json
import re





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


def selectionArray(room, time, date):
    room_data = room
    time_data = time
    res_date = date
    choice_array = []
    new_dict = {date: {room_data, time_data}}

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

    reservation = selectionArray(selected_room, selected_time, specific_date)

    if request.method == 'POST':
        if not any(d == reservation for d in array_choice):
            array_choice.append(reservation)
            
        context = {
            'reservation': reservation,
            'choices': array_choice,
            'results': results,
            'specific_date': specific_date,
        }

        return render(request, template, context)

    context = {
        'reservation': reservation,
        'choices': array_choice,
        'results': results,
        'specific_date': specific_date,
    }
  

    return render(request, template, context)


def SelectedRoomList(list):
    combo_list = list
    if not any(d == new_choice for d in combo_list):
        combo_list.append(new_choice)

    return combo_list

def ReturnArray(input):
    new_input = input
    result = ast.literal_eval(new_input)

    return result

def BookingData(request):
    template = 'page3.html'
    game_list = request.POST['list_choices']
    game_array = ReturnArray(game_list)
    game_update = TestForm(data=request.POST)
    date = '2023-05-07'
    time = '18:00'
    room = 'Pirate'
    
    
    game_form = TestForm()
    if request.method == 'POST':
        game_form = TestForm(data=request.POST)
        if game_form.is_valid():
            new_game = game_form.save(commit=False)
            new_game.date = date
            new_game.time = time
            new_game.room = room
            new_game.save()
            return redirect('home')
    else:
        return redirect('reservation')



    context = {
        'choices': game_array,
        'form': game_update,
    }

    return render(request, template, context)


def Posted(request):
    template = 'posted.html'

    return render(request, template)


def BookingSubmit(request):
    template = 'page3.html'
    game_list = request.POST['list_choices']
    game_array = ReturnArray(game_list)
    form = TestForm()

    context = {
        'form': form,
        'choices': game_array,
    }

    return render(request, template, context)
    
    if request.method == 'POST':
        for item in game_array:
            details = item[0].popitem()
            date, times_and_rooms = details
            time, room = tuple(times_and_rooms)
            reservation = TestModel(date=date, time=time, room=room)
            form = TestForm(request.POST)
            if form.is_valid():
                booking_model = form.save(commit=False)
                booking_model.date = date
                booking_model.time = time
                booking_model.room = room
                booking_model.save()
                redirect('posted')

  
    
        
    


def Test2(request):
    template = 'test2.html'

    return render(request, template)

def VarCreation(booking_data):
    details = booking_data[0].popitem()
    date, times_and_rooms = details
    time, room = tuple(times_and_rooms)
    
    return date, time, room


def UpdateReservation(game_array, form):
    if request.method == 'POST':
        for item in game_array:
            details = item[0].popitem()
            date, times_and_rooms = details
            time, room = tuple(times_and_rooms)
            form = TestForm(request.POST)
            if form.is_valid():
                booking_model = form.save(commit=False)
                booking_model.date = date
                booking_model.time = time
                booking_model.room = room
                booking_model.save()


def testUpdage(request):
    template = "page3.html"
    date = '2023-05-10'
    time = '18:00'
    room = 'Pirate'
    name = 'name'
    email = 'email'

    form = TestForm()
    context = {'form': form}  
    
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            # create a TestModel instance and save it
            test_model = form.save(commit=False)
            test_model.name = name
            test_model.email = email
            test_model.date = date
            test_model.time = time
            test_model.room = room
            test_model.save()
            return redirect('posted')
        else: 
            return redirect('home')
        
        context = {'form': form}
        return render(request, template, context)
      
    return render(request, template, context)


class ResUpdates(View):

    def get(self, request):
        template = 'page2.html'
        selected_room = request.POST.get['key']
        selected_time = request.POST.get['value']
        specific_date = request.POST.get['selected_date']
        choice_list = request.POST.get['choices']
        array_choice = ReturnArray(choice_list)
        specific_times = Time.objects.all()
        room_list = Room.objects.all()
        results = dayView(room_list, specific_date, specific_times)
        reservation = selectionArray(selected_room, selected_time, specific_date)

        context = {
            'reservation': reservation,
            'choices': array_choice,
            'results': results,
            'specific_date': specific_date,
        }
            
        return render(request, template, context)

    def post(self, request):
        template = "page3.html"

        return render(request, template)

class NewPageView(FormView):
    form_class = MyForm
    template_name = 'page1.html'

    def page_load():
        specific_date = '2023-05-07'
        specific_times = Time.objects.all()
        room_list = Room.objects.all()

        results = dayView(room_list, specific_date, specific_times)
        context = {
            'selected_date': specific_date,
            'results': results,
            'choices': choices
        }

        return render(request, template, context)

    def form_valid(self, form):
        # Redirect to the ResUpdate view with hidden input values
        return super().form_valid(form)

    def get_success_url(self):
        selected_key = self.request.POST.get('key')
        selected_value = self.request.POST.get('value')
        specific_date = self.request.POST.get('specific_date')
        url = reverse('res_update')
        url += f'?selected_key={key}&selected_value={value}&specific_date={specific_date}'
        return url


class RoomSelection(View):

    def get(self, request):
        template = 'page1.html'
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

    def post(self, request):
        selected_room = request.POST.get('key')
        selected_time = request.POST.get('value')
        specific_date = request.POST.get('selected_date')
        choices = request.POST.get('choices')
        url = reverse('reservation_update', kwargs={'selected_room': selected_room, 'selected_time': selected_time, 'specific_date': specific_date, 'choices': choices})
        return redirect(url)
        # return redirect('reservation', selected_room=selected_room, selected_time=selected_time, specific_date=specific_date, choices=choices)

class ResUpdate(View):

    def get(self, request, selected_room, selected_time, specific_date, choices):
        template = 'page2.html'
        # Your code for the get function here using selected_room, selected_time, specific_date variables
        specific_times = Time.objects.all()
        room_list = Room.objects.all()
        results = dayView(room_list, specific_date, specific_times)
        reservation = selectionArray(selected_room, selected_time, specific_date)

        context = {
            'reservation': reservation,
            'choices': choices,
            'results': results,
            'specific_date': specific_date,
        }

        return render(request, template, context)

    def post(self, request):
        template = "page3.html"
        # Your code for the post function here
        return render(request, template)


class FirstView(View):
    def get(self, request):
        template = 'test1.html'

        return render(request, template)

    def post(self, request):
        var1 = request.POST.get('var1')
        var2 = request.POST.get('var2')
        # Do some processing with my_variable
        return redirect('second_view', var1=var1, var2=var2)

class SecondView(View):
    template = 'test2.html'
    array = []

    def get(self, request, var1, var2):
        template = 'test2.html'
        # Do some processing with my_variable
        words = list((var1, var2))
          
        if not any(d == words for d in self.array):
            self.array.append(words)

        return render(request, template, {'var1': var1, 'var2': var2, 'array': self.array})

    def post(self, request, var1, var2):
        if request.POST.get('action') == 'submit1':
            var1 = request.POST.get('var1')
            var2 = request.POST.get('var2')
            words = list((var1, var2))
          
            if not any(d == words for d in self.array):
                self.array.append(words)
            return render(request, self.template, {'var1': var1, 'var2': var2, 'array': self.array})
        if request.POST.get('action') == 'submit2':
            our_variable = request.POST.get('our_variable')
            return redirect('third_view', our_variable=our_variable)

class ThirdView(View):

    def get(self, request, our_variable):
        template = 'test3.html'

        return render(request, template, {'our_variable': our_variable})

class AvailableGames(View):

    def get(self, request):
        template = 'test1.html'
        specific_date = '2023-05-07'
        specific_times = Time.objects.all()
        room_list = Room.objects.all()
        results = dayView(room_list, specific_date, specific_times)
        context = {
            'selected_date': specific_date,
            'results': results,
        }

        return render(request, template, context)

    def post(self, request):
        template = 'test1.html'
        array = []
        selected_room = request.POST.get('key')
        selected_time = request.POST.get('value')
        specific_date = request.POST.get('selected_date')
        return redirect('selected_games', selected_room=selected_room, selected_time=selected_time, specific_date=specific_date, array=array)

class SelectedGames(View):
    template = 'test2.html'
    def get(self, request, selected_room, selected_time, specific_date, array):
        specific_times = Time.objects.all()
        room_list = Room.objects.all()
        results = dayView(room_list, specific_date, specific_times)

        url = request.path
        game_list = url_work(url)
        game_array = request.session.get('game_array')

        if not any(d == game_list for d in game_array):
                game_list.append(game_array)
        request.session['game_array'] = game_array
        
        return render(request, self.template, {'selected_room': selected_room, 'selected_time': selected_time, 'specific_date': specific_date, 'results': results, 'game_array': game_array})

    def post(self, request, selected_room, selected_time, specific_date, array):
        if request.POST.get('action') == "submit1":
            selected_room = request.POST.get('key')
            selected_time = request.POST.get('value')
            specific_date = request.POST.get('specific_date')
            array = request.POST.getlist('game_array')
            request.session['game_array'] = array
            return redirect('selected_games', selected_room=selected_room, selected_time=selected_time, specific_date=specific_date, array=array)


            # game_list = request.POST.getlist('test_data')
            # url = request.path
            # new_test_data = url_work(url)
            # if not any(d == new_test_data for d in game_list):
            #     new_test_data.append(game_list)

            # return render(request, self.template, {'game_list': game_list, 'results': results})

            # selected_room = request.POST.get('key')
            # selected_time = request.POST.get('value')
            # specific_date = request.POST.get('selected_date')
            # my_array = request.POST.getlist('test_data')
            # game_choice = list((specific_date,selected_room,selected_time))        

            # if not any(d == game_choice for d in my_array):
            #     my_array.append(game_choice)
            
            
            # return redirect('selected_games', selected_room=selected_room, selected_time=selected_time, specific_date=specific_date)

            # return render(request, self.template, {'selected_room': selected_room, 'selected_time': selected_time, 'specific_date': specific_date, 'my_array': my_array})
            # return render(request, self.template, {'selected_room': selected_room, 'selected_time': selected_time, 'specific_date': specific_date, 'array':array})


# def parse_url(url):
#     pattern = r'^selected_games/(\w+)/(\w+)/(\w+)/$'
#     match = re.match(pattern, url)
#     if match:
#         return [match.group(1), match.group(2), match.group(3)]
#     else:
#         return []

def url_work(url):
    # extract the path from the URL
    path = re.search(r"/selected_games/(.*)", url).group(1)
    
    # split the path into parts
    path_array = path.split("/")
    
    # extract the game data
    selected_room = path_array[0]
    selected_time = path_array[1]
    specific_date = path_array[2]

    game_item = [selected_room, selected_time, specific_date]
    print(game_item)
    return game_item



        # array = [game_choice]
        # if not any(d == game_choice for d in array):
        #     game_choice.append(array) 


class ShoppingView(View):
    def get(self, request):
        # Get the items to display on the page
        specific_date = '2023-05-07'
        specific_times = Time.objects.all()
        room_list = Room.objects.all()
        results = dayView(room_list, specific_date, specific_times)

        context = {'results': results, 'specific_date': specific_date}
        return render(request, 'shopping.html', context)
    
    def post(self, request):
        # # Get the information about the item the user wants to add to their cart
        # key = request.POST.get('key')
        # value = request.POST.get('value')
        # specific_date = request.POST.get('specific_date')
        
        # # Create a dictionary to represent the item and add it to the user's cart
        # item = {'key': key, 'value': value, 'specific_date': specific_date}
        # request.session.setdefault('cart', []).append(item)
        
        # # Get the updated items to display on the page, including the user's cart
        # specific_date = '2023-05-07'
        # specific_times = Time.objects.all()
        # room_list = Room.objects.all()
        # results = dayView(room_list, specific_date, specific_times)
        # cart = request.session.get('cart', [])
        # context = {'results': results, 'cart': cart, "specific_date": specific_date}
        # return render(request, 'shopping.html', context)
    # Get the information about the item the user wants to add to their cart
        key = request.POST.get('key')
        value = request.POST.get('value')
        specific_date = request.POST.get('specific_date')

        # Check if the item is already in the cart
        cart = request.session.get('cart', [])
        for item in cart:
            if item['key'] == key and item['value'] == value and item['specific_date'] == specific_date:
                # If the item already exists in the cart, do not add it again
                break
        else:
            # If the item does not exist in the cart, add it to the cart
            item = {'key': key, 'value': value, 'specific_date': specific_date}
            cart.append(item)
            request.session['cart'] = cart


        if 'delete-all' in request.POST:
            # Remove all items from the cart
            request.session.pop('cart', None)
        elif 'delete-item' in request.POST:
            # Get the key, value, and specific_date of the item to remove
            selected = request.POST.get('delete-item')
            key, value, specific_date = selected.split("|")
            # Find the item in the cart and remove it
            for item in request.session.get('cart', []):
                if item['key'] == key and item['value'] == value and item['specific_date'] == specific_date:
                    request.session['cart'].remove(item)
                    request.session.modified = True

                    break
        # Get the updated items to display on the page, including the user's cart


        specific_date = '2023-05-07'
        specific_times = Time.objects.all()
        room_list = Room.objects.all()
        results = dayView(room_list, specific_date, specific_times)
        cart = [item for item in request.session.get('cart', []) if item.get('key') and item.get('value') and item.get('specific_date')]
        context = {'results': results, 'cart': cart, "specific_date": specific_date}
        return render(request, 'shopping.html', context)

class BookingsView(View):
    def get(self, request):
        cart = request.session.get('cart', [])
        context = {'cart': cart}
        return render(request, 'booking.html', context)

def CartView(request):
    cart = request.GET.get('cart')
    string = cart.replace('[', '').replace(']', '').replace('"', '')
    game_data = ast.literal_eval(string)
    if isinstance(game_data, dict):
    # if dataset is a dictionary, convert it to a tuple
        dataset = (game_data,)
    else:
        dataset = game_data
    context = {'cart': cart, 'string': string, 'data': dataset,}
    return render(request, 'booking.html', context, )

def update_database(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        date = request.POST.get('date')
        room = request.POST.get('room')
        time = request.POST.get('time')

        # Create a new instance of the TestModel and set its attributes
        instance = TestModel()
        instance.name = name
        instance.email = email
        instance.date = date
        instance.room = room
        instance.time = time
        instance.save()

        return HttpResponse('Data saved successfully.')

    # If the request method is not POST, return an empty form
    return render(request, 'update_database.html')
    
    #     if form.is_valid():
    #         instance = form.save(commit=False)
    #         instance.name = request.POST.get('name')
    #         instance.email = request.POST.get('email')
    #         instance.date = request.POST.get('date')
    #         instance.room = request.POST.get('room')
    #         instance.time = request.POST.get('time')
    #         instance.save()
    #         return HttpResponse('Data saved successfully.')
        
    # return render(request, 'booking.html', {'form': form})

def countData(dict):
    my_dict = dict
    count = 0
    for value in my_dict.values():
        if isinstance(value, str):
            count += 1

    return count

def testMore(data):
    my_tuple = tuple(my_dict.items())
    return my_tuple


class UpdateBooking(View):
    template_name = 'booking.html'

    def get(self, request, *args, **kwargs):
        cart = request.GET.get('cart')
        string = cart.replace('[', '').replace(']', '').replace('"', '')
        game_data = ast.literal_eval(string)
        if isinstance(game_data, dict):
            dataset = (game_data,)
        else:
            dataset = game_data
        context = {'cart': cart, 'string': string, 'data': dataset}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = TestForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.date = request.POST.get('date')
            instance.room = request.POST.get('room')
            instance.time = request.POST.get('time')
            instance.save()
            return HttpResponse('Data saved successfully.')
        return render(request, self.template_name, {'form': form})