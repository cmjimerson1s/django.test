from . import views
from .views import ResUpdate
from django.views import View
from django.urls import path



urlpatterns = [
    path('', views.ShoppingView.as_view(), name='home'),
    # path('', views.FirstView.as_view(), name='home'),
    # path('second_view/<str:var1>/<str:var2>', views.SecondView.as_view(), name='second_view'),
    path('selected_games/<str:selected_room>/<str:selected_time>/<str:specific_date>/<str:array>', views.SelectedGames.as_view(), name='selected_games'),
    path('third_view/<str:our_variable>', views.ThirdView.as_view(), name='third_view'),
    # path('booking', views.BookingsView.as_view(), name='booking'),
    path('booking', views.CartView, name='booking'),
    path('posted', views.update_database, name='posted')
]

    # path('update/<str:selected_room>/<str:selected_time>/<str:specific_date>/', ResUpdate.as_view(), name='reservation_update'),
    # path('reservation_multi', views.MultiViewResList, name='reservation_multi'),
    # path('booking', views.ResUpdate.as_view(), name="booking"),