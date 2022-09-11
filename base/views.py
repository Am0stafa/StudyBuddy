#! when someone goes to a specific url these are going to be functions or classes which will fire off this like queries to the database , any templates that we need to render. this is whats going to be called when someone goes to a specific url

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("home page")


def room(request):
    return HttpResponse("rooms page")