# the_flag_intranet/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls), # Die Verwaltungsoberfläche für HR (Kategorie C)
    path('', include('intranet_app.urls')), # Leitet alle Anfragen an unsere Intranet-App weiter
]
