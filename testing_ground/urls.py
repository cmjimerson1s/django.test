from . import views
from django.urls import path

urlpatterns = [
    path('', views.resultView, name='home'),
    path('reservation', views.choiceView, name='reservation')
] 