# the_flag_intranet/urls.py

from django.contrib import admin
from django.urls import path, include
from intranet_app.views import home
# NEU: Wir importieren die Standard-Logout-View
from django.contrib.auth.views import LogoutView 


urlpatterns = [
    # Admin-Bereich
    path('admin/', admin.site.urls),
    
    # Unsere Haupt-App
    path('', home, name='home'),
    
    # Standard-Pfade für Anmeldung/Passwort-Zurücksetzung
    # (Enthält login/)
    path('accounts/', include('django.contrib.auth.urls')),
    
    # NEU: Wir definieren den Logout-Pfad explizit
    # Wenn Django diesen Pfad sieht, leitet er automatisch zu LOGOUT_REDIRECT_URL weiter
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
]

# WICHTIG: Die URL 'accounts/logout/' muss nach dem 'include('django.contrib.auth.urls')' stehen!
