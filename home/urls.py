from django.urls import path

from home import views

urlpatterns = [
    #path('fr/', views.index, name='home_page')
    path('', views.index, name='home_page'),

]
