from django.shortcuts import render,redirect
from django.urls import path,include
from Guest import views
app_name="Guest"

urlpatterns = [
    path('AjaxPlace/',views.ajaxplace,name="ajaxplace"),
    path('UserRegistration/',views.UserRegistration,name="UserRegistration"),
    path('Login/',views.Login,name="Login"),
    path('RenterRegistration/',views.RenterRegistration,name="RenterRegistration"),
    path('RepairshopRegistration/',views.RepairshopRegistration,name="RepairshopRegistration"),
    path('',views.index,name="index")
]
