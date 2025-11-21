# intranet_app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UrlaubsAntrag, Mitarbeiter, Krankmeldung # Alle unsere Datenbank-Modelle

# --- WICHTIGE HINWEISE ---
# Dieser Code dient als Platzhalter. Ein Programmierer muss die
# Logik zur Berechnung der Urlaubstage (ohne Wochenenden/Feiertage)
# und das E-Mail-System hier noch implementieren.
# -------------------------


def home(request):
    """Zeigt die Startseite / das Dashboard an."""
    # Hier wird die Logik aus Schritt 9 ("Der Türsteher") implementiert
    return render(request, 'intranet_app/home.html', {'user': request.user})

@login_required
def urlaub_antrag(request):
    """Seite zum Stellen eines Urlaubsantrags."""
    # Hier kommt die Logik für die Formularverarbeitung und die Prüfungen
    return render(request, 'intranet_app/urlaub_antrag.html', {})

@login_required
def antraege_uebersicht(request):
    """Übersicht für Vorgesetzte (Kategorie B & C) zur Genehmigung."""
    if request.user.kategorie in ['B', 'C']:
        # Filtert alle Anträge, die auf Genehmigung warten und für diesen Chef sind
        offene_antraege = UrlaubsAntrag.objects.filter(
            mitarbeiter__vorgesetzter=request.user, 
            status='NEU'
        )
        return render(request, 'intranet_app/antraege_uebersicht.html', {'antraege': offene_antraege})
    else:
        # Kein Zugriff für Kategorie A
        return redirect('home')

@login_required
def personalakte_detail(request, user_id):
    """Detailansicht der Personalakte (Nur für Kategorie C)."""
    if request.user.kategorie == 'C':
        mitarbeiter = Mitarbeiter.objects.get(pk=user_id)
        return render(request, 'intranet_app/personalakte_detail.html', {'mitarbeiter': mitarbeiter})
    else:
        # Kein Zugriff
        return redirect('home')
