from django.urls import path

from . import views

app_name = "Apps.pos"
urlpatterns = [
    path('', views.index, name='index'),
]
