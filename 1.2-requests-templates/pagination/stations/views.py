import csv
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    bus_stations = []
    with open(settings.BUS_STATION_CSV,  newline='', encoding='utf8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            station = {}
            station['Name'] = row['Name']
            station['Street'] = row['Street']
            station['District'] = row['District']
            bus_stations.append(station)
    paginator = Paginator(bus_stations, 20)
    page_number = int(request.GET.get('page', 1))
    page = paginator.get_page(page_number)
    context = {
        'bus_stations': page,
        'page': page,
    }
    return render(request, 'stations/index.html', context)
