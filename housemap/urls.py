"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from django.conf import settings
from django.conf.urls.static import static

from housemanage.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('housemanage/', include('housemanage.urls')),
    path('addhouse/', include('housemanage.urls')),
    path('deletehouse/', include('housemanage.urls')),
    path('changehouse/', include('housemanage.urls')),
    path('/', include('housemanage.urls'), name='index'),
    path('', include('housemanage.urls')),
]
if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
