from . import views
from django.urls import path

urlpatterns = [
    path('', views.Page1, name='home'),
    path('reservation', views.Page2, name='reservation'),
    path('reservation_multi', views.MultiViewResList, name='reservation_multi')
] 