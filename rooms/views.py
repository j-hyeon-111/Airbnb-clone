from django.shortcuts import render
from . import models


def all_rooms(request):
    all_rooms = models.Room.objects.all()[:5]
    return render(request, "rooms/home.html", context={"home": all_rooms})
