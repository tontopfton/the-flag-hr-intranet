from django.db import models
from django.contrib.auth.models import AbstractUser

# --- DEFINITION DER MITARBEITER-MODELLE ---

class Mitarbeiter(AbstractUser):
    # Felder aus dem Lastenheft Punkt 4.10 und Definitionen
    KATEGORIE_CHOICES = [
        ('A', 'Kategorie A: Arbeitnehmer'),
        ('B', 'Kategorie B: Führungskraft'),
        ('C', 'Kategorie C: HR/Geschäftsführung'),
    ]
    GESELLSCHAFT_CHOICES = [
        ('RES', 'Residential'),
        ('FRA', 'Service Frankfurt'),
        ('MUC', 'Service München'),
        ('HLD', 'Holding'),
    ]

    # --- Stammdaten & Kategorie ---
    kategorie = models.CharField(max_length=1, choices=KATEGORIE_CHOICES, default='A')
    gesellschaft = models.CharField(max_length=3, choices=GESELLSCHAFT_CHOICES)
    tätigkeit = models.CharField(max_length=100)
    standort = models.CharField(max_length=100)
    geburtsdatum = models.DateField(null=True, blank=True)
    eintrittsdatum = models.DateField(null=True, blank=True)
    vollzeit_teilzeit = models.CharField(max_length=50) # VZ/TZ
    
    # --- Gehalt & Bonus ---
    monatsgehalt = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    jahresgehalt = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    bonus_anspruch = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # --- Urlaub ---
    urlaubstage_gesamt = models.IntegerField(default=30)
    resturlaub = models.DecimalField(max_digits=4, decimal_places=1, default=30)
    
    # --- Ausstattung & Sonstiges ---
    arbeitsmittel = models.TextField(blank=True)
    schluessel = models.TextField(blank=True)
    auto = models.CharField(max_length=100, blank=True)
    besonderheiten = models.TextField(blank=True)
    
    # --- Hierarchie & Notfall ---
    vorgesetzter = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    notfallkontakt_name = models.CharField(max_length=100, blank=True)
    notfallkontakt_nummer = models.CharField(max_length=50, blank=True)
    
    # --- Onboarding-Status ---
    onboarding_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.last_name}, {self.first_name} ({self.tätigkeit})"

# --- 1. URLAUBSANTRAG ---
class UrlaubsAntrag(models.Model):
    mitarbeiter = models.ForeignKey(Mitarbeiter, on_delete=models.CASCADE, related_name='urlaubsantraege')
    von_datum = models.DateField()
    bis_datum = models.DateField()
    ist_halber_tag = models.BooleanField(default=False) # Für 24.12. und 31.12.

    STATUS_CHOICES = [
        ('NEU', 'Neu eingereicht / Wartet auf Chef'),
        ('GENEHMIGT', 'Genehmigt'),
        ('ABGELEHNT', 'Abgelehnt'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEU')
    kommentar_vorgesetzter = models.TextField(blank=True)

# --- 2. KRANKMELDUNG ---
class Krankmeldung(models.Model):
    mitarbeiter = models.ForeignKey(Mitarbeiter, on_delete=models.CASCADE)
    von_datum = models.DateField()
    bis_datum = models.DateField(null=True, blank=True)
    dokument = models.FileField(upload_to='krankmeldungen/%Y/%m/', blank=True)
    
# --- 3. ZIELVEREINBARUNGEN ---
class Zielvereinbarung(models.Model):
    mitarbeiter = models.ForeignKey(Mitarbeiter, on_delete=models.CASCADE)
    vorgesetzter = models.ForeignKey(Mitarbeiter, related_name='betreute_ziele', on_delete=models.SET_NULL, null=True)
    jahr = models.IntegerField()
    bonus_anspruch_euro = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Status
    ist_unterschrieben_ma = models.BooleanField(default=False)
    ist_unterschrieben_chef = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default='LAUFEND')

class EinzelZiel(models.Model):
    vereinbarung = models.ForeignKey(Zielvereinbarung, on_delete=models.CASCADE, related_name='ziele')
    beschreibung = models.TextField()
    gewichtung_prozent = models.IntegerField()
    ist_erreicht = models.BooleanField(default=False)

# --- 4. DIENSTREISEN ---
class DienstreiseAntrag(models.Model):
    mitarbeiter = models.ForeignKey(Mitarbeiter, on_delete=models.CASCADE)
    von_datum = models.DateField()
    bis_datum = models.DateField()
    reiseziel = models.CharField(max_length=200)
    reisezweck = models.TextField()
    verkehrsmittel = models.CharField(max_length=100)
    
    # Mehrstufiger Status (Vorgesetzter und ggf. GF)
    STATUS_CHOICES = [
        ('NEU', 'Wartet auf Vorgesetzten'),
        ('GENEHMIGT_V', 'Vorgesetzter OK - Wartet auf GF'),
        ('GENEHMIGT_FINAL', 'Endgültig Genehmigt'),
        ('ABGELEHNT', 'Abgelehnt'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEU')
    
# --- 5. ONBOARDING (Die Checkliste) ---
class OnboardingProzess(models.Model):
    mitarbeiter = models.OneToOneField(Mitarbeiter, on_delete=models.CASCADE)
    private_email = models.EmailField()
    ist_abgeschlossen = models.BooleanField(default=False)

class OnboardingPunkt(models.Model):
    prozess = models.ForeignKey(OnboardingProzess, related_name='punkte', on_delete=models.CASCADE)
    bezeichnung = models.CharField(max_length=200)
    vorlage_datei = models.FileField(upload_to='onboarding/vorlagen/')
    ausgefuellte_datei = models.FileField(upload_to='onboarding/uploads/', blank=True, null=True)
    erledigt = models.BooleanField(default=False)
