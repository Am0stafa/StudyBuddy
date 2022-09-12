from django.contrib import admin

# Register your models here.
from .models import Room, Topic, Message

#! we are basically saying to the admin panel that we want to be able to view this item and also work with it in the built in admin panel

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)