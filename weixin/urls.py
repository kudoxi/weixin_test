from django.urls import path
from . import views

urlpatterns = [
    #path('index/',views.index,name="index"),
    path('access_token',views.access_token,name="access_token"),
]
