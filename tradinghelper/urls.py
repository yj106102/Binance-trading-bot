from django.urls import path

from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('create/',views.create_strategy),
    path('stop/',views.stop),
    path('records/',views.records)
]