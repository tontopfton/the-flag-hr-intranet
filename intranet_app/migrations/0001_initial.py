# intranet_app/migrations/0001_initial.py

import django.contrib.auth.models
import django.contrib.auth.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mitarbeiter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('kategorie', models.CharField(choices=[('A', 'Kategorie A: Arbeitnehmer'), ('B', 'Kategorie B: Führungskraft'), ('C', 'Kategorie C: HR/Geschäftsführung')], default='A', max_length=1)),
                ('gesellschaft', models.CharField(choices=[('RES', 'Residential'), ('FRA', 'Service Frankfurt'), ('MUC', 'Service München'), ('HLD', 'Holding')], max_length=3)),
                ('tätigkeit', models.CharField(max_length=100)),
                ('standort', models.CharField(max_length=100)),
                ('geburtsdatum', models.DateField(blank=True, null=True)),
                ('eintrittsdatum', models.DateField(blank=True, null=True)),
                ('vollzeit_teilzeit', models.CharField(max_length=50)),
                ('monatsgehalt', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('jahresgehalt', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('bonus_anspruch', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('urlaubstage_gesamt', models.IntegerField(default=30)),
                ('resturlaub', models.DecimalField(decimal_places=1, default=30, max_digits=4)),
                ('arbeitsmittel', models.TextField(blank=True)),
                ('schluessel', models.TextField(blank=True)),
                ('auto', models.CharField(blank=True, max_length=100)),
                ('besonderheiten', models.TextField(blank=True)),
                ('notfallkontakt_name', models.CharField(blank=True, max_length=100)),
                ('notfallkontakt_nummer', models.CharField(blank=True, max_length=50)),
                ('onboarding_complete', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('vorgesetzter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='DienstreiseAntrag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('von_datum', models.DateField()),
                ('bis_datum', models.DateField()),
                ('reiseziel', models.CharField(max_length=200)),
                ('reisezweck', models.TextField()),
                ('verkehrsmittel', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('NEU', 'Wartet auf Vorgesetzten'), ('GENEHMIGT_V', 'Vorgesetzter OK - Wartet auf GF'), ('GENEHMIGT_FINAL', 'Endgültig Genehmigt'), ('ABGELEHNT', 'Abgelehnt')], default='NEU', max_length=20)),
                ('mitarbeiter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Krankmeldung',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('von_datum', models.DateField()),
                ('bis_datum', models.DateField(blank=True, null=True)),
                ('dokument', models.FileField(blank=True, upload_to='krankmeldungen/%Y/%m/')),
                ('mitarbeiter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OnboardingProzess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('private_email', models.EmailField(max_length=254)),
                ('ist_abgeschlossen', models.BooleanField(default=False)),
                ('mitarbeiter', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OnboardingPunkt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bezeichnung', models.CharField(max_length=200)),
                ('vorlage_datei', models.FileField(upload_to='onboarding/vorlagen/')),
                ('ausgefuellte_datei', models.FileField(blank=True, null=True, upload_to='onboarding/uploads/')),
                ('erledigt', models.BooleanField(default=False)),
                ('prozess', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='punkte', to='intranet_app.onboardingprozess')),
            ],
        ),
        migrations.CreateModel(
            name='UrlaubsAntrag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('von_datum', models.DateField()),
                ('bis_datum', models.DateField()),
                ('ist_halber_tag', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('NEU', 'Neu eingereicht / Wartet auf Chef'), ('GENEHMIGT', 'Genehmigt'), ('ABGELEHNT', 'Abgelehnt')], default='NEU', max_length=20)),
                ('kommentar_vorgesetzter', models.TextField(blank=True)),
                ('mitarbeiter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='urlaubsantraege', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Zielvereinbarung',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jahr', models.IntegerField()),
                ('bonus_anspruch_euro', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ist_unterschrieben_ma', models.BooleanField(default=False)),
                ('ist_unterschrieben_chef', models.BooleanField(default=False)),
                ('status', models.CharField(default='LAUFEND', max_length=20)),
                ('mitarbeiter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vorgesetzter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='betreute_ziele', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EinzelZiel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beschreibung', models.TextField()),
                ('gewichtung_prozent', models.IntegerField()),
                ('ist_erreicht', models.BooleanField(default=False)),
                ('vereinbarung', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ziele', to='intranet_app.zielvereinbarung')),
            ],
        ),
    ]
