# intranet_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), # Startseite (Dashboard)
    path('urlaub/antrag/', views.urlaub_antrag, name='urlaub_antrag'),
    path('genehmigen/', views.antraege_uebersicht, name='antraege_uebersicht'),
    path('personalakte/<int:user_id>/', views.personalakte_detail, name='personalakte_detail'),
    # Hier werden später weitere Routen für Krank, Reisen, Ziele hinzugefügt
]
