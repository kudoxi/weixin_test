from django.urls import path
from . import views

urlpatterns = [
    #path('index/',views.index,name="index"),
    path('access_token',views.index,name="access_token"),
]
