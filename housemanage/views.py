from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.urls import reverse

from .models import *
from .forms import *

from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
import json
import datetime

def index(request):
    user = request.user
    
    now = timezone.now()
    DAY = timezone.timedelta(days=1)
    MINUTE = timezone.timedelta(minutes=1)
    
    try:
        houses = list(House.objects.order_by('location'))
    except:
        houses = []
    try:
        basemap1 = Basemap.objects.get(default=True)
        basemap2 = Basemap.objects.filter(default=False)
        basemaps = [basemap1] + list(basemap2)
    except:
        basemap1 = Basemap()
        basemap2 = Basemap()
        basemaps = [basemap1, basemap2]   
    try:
        token = AccessToken.objects.get(name='googlemap')
        token = token.token
    except:
        token = ''
    form = HouseForm()
    lat = request.session.get('lat', None)
    lon = request.session.get('lon', None)
    request.session['lat'] = None
    request.session['lon'] = None
    new_house = None

    deleted = request.session.get('deleted', None)
    request.session['deleted'] = None
    return render(request, 'housemanage/index.html', {'houses':     houses,
                                                    'token':      token,
                                                    'basemaps':   basemaps,
                                                    'form':       form,
                                                    'new_house':  new_house,
                                                    'lat':        lat,
                                                    'lon':        lon,
                                                    'GOOGLE_MAP_KEY': settings.GOOGLE_MAP_KEY
                                                })
def addhouse(request):
    if request.method == 'POST':
        form = HouseForm(request.POST)
        if form:
            new_house = form.save(commit=False)
            new_house.save()
            request.session['modified'] = new_house.location
            request.session['lat'] = new_house.latitude
            request.session['lon'] = new_house.longitude
            return redirect('/')
        else:
            return redirect('/')
    else:
        return render(request, 'housemanage/index.html')
    

def deletehouse(request):
    pk = request.POST.get('pk')
    pt = get_object_or_404(Point, pk=pk)
    request.session['lat'] = pt.latitude
    request.session['lon'] = pt.longitude
    request.session['zoom'] = 13
    if request.user == pt.user:
        pt.delete()
        request.session['deleted'] = pt.location
    return redirect('/')

def changehouse(request):
    ptpk = request.POST.get('ptpk')
    pt = get_object_or_404(Point, pk=ptpk)
    request.session['lat'] = pt.latitude
    request.session['lon'] = pt.longitude
    request.session['zoom'] = 13
    if request.user == pt.user:
        allpks = Category.objects.all().values_list('pk', flat=True)
        for pk in allpks:
            catpk = request.POST.get('catpk_'+str(pk)+'.x')
            if catpk:
                cat = get_object_or_404(Category, pk=pk)
                pt.category = cat
                pt.save()
                request.session['modified'] = pt.location
                return redirect('/')
    return redirect('/')
def showhouse(request, id=1):
    house = House.objects.get(id=id)
    return render(request, 'housemanage/showhouse.html', {'house': house,'GOOGLE_MAP_KEY': settings.GOOGLE_MAP_KEY})