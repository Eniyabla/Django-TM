from django.urls import path

from place import views

urlpatterns = [
    path('ratePlace/<int:id>/', views.ratePlace, name='ratePlace'),
    path('', views.place, name='user_place'),

]
