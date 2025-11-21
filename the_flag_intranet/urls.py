# the_flag_intranet/urls.py

from django.contrib import admin
from django.urls import path, include
from intranet_app.views import home
# WICHTIG: Die Zeile 'from django.contrib.auth.views import LogoutView' entfernen, falls sie noch existiert!

urlpatterns = [
    # Admin-Bereich
    path('admin/', admin.site.urls),
    
    # Unsere Haupt-App
    path('', home, name='home'),
    
    # Standard-Pfade für Anmeldung/Abmeldung/Passwort-Zurücksetzung
    # (Enthält login/ und logout/, sowie die automatische Weiterleitung)
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Die explizite 'logout'-Zeile WIRD ENTFERNT, da sie redundant ist.
]
