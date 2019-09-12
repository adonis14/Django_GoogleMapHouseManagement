from django.db import models
from django.forms import ModelForm, HiddenInput
from django.contrib.auth.models import User, Group
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _ # _() this function is for print string

# Create your models here.
basemapNameValidator = RegexValidator(r'^[A-Z][a-zA-Z]*$',
                                      'Must start with A-Z and contain only letters.')

class House(models.Model):
    location  = models.CharField(max_length=280) # address string
    latitude  = models.FloatField()
    longitude = models.FloatField()
    def __str__(self):
        return self.location
    class Meta:
        verbose_name        = "location"
        verbose_name_plural = "locations"
class HouseDetail(models.Model):
    housepk = models.ForeignKey(House,on_delete=models.CASCADE)
    def __str__(self):
        return self.housepk
    
class HouseForm(ModelForm):
    class Meta:
        model = House
        fields = ['location', 'latitude', 'longitude']
        labels = {
            'location': _('Location Name'),
        }
        widgets = {'latitude': HiddenInput(), 'longitude': HiddenInput()}
    def __init__(self, *args, **kwargs):
        super(HouseForm, self).__init__(*args, **kwargs)
        self.fields['location'].widget.attrs['placeholder'] = 'Please enter the location'
        self.fields['location'].widget.attrs['disabled'] = True
class AccessToken(models.Model):
    name  = models.CharField(max_length=280)
    token = models.CharField(max_length=280)
    def __str__(self):
        return self.name
        
class Basemap(models.Model):
    name    = models.CharField(max_length=20,
                               validators=[basemapNameValidator],
                               unique=True)
    tileURL = models.CharField(max_length=280)
    default = models.BooleanField(default=False)
    def __str__(self):
        return self.name