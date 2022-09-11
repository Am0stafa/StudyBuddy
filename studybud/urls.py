#! this is all the url routing to our project when you go to a certain page this is where we configure all the url so its going to be just a list of all the different url paths

"""studybud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include


#! to create a view

urlpatterns = [
    path('admin/', admin.site.urls),
    #! we want to tell django when we go to the website this file is going to handle all the core url routing 
    path('',include('base.urls'))
]





