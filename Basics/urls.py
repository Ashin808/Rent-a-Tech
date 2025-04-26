from django.urls import path,include
from Basics import views

urlpatterns = [
    path('Add/',views.add,name="Add"),
    path('Largest/',views.largest,name="Largest"),
    path('Calculator/',views.Calculator,name="Calculator"),
    path('largestandsmallest/',views.largestandsmallest,name="largestandsmallest")

]