import csv

from django.shortcuts import render
from .models import Dht11  # Assurez-vous d'importer le modèle Dht11
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
import datetime


def table(request):
    derniere_ligne = Dht11.objects.last()

    if derniere_ligne is not None:  # Vérifier si la table n'est pas vide
        derniere_date = derniere_ligne.dt
        delta_temps = timezone.now() - derniere_date
        difference_minutes = delta_temps.seconds // 60

        if difference_minutes > 60:
            temps_ecoule = 'il y a ' + str(difference_minutes // 60) + 'h' + str(difference_minutes % 60) + 'min'
        else:
            temps_ecoule = 'il y a ' + str(difference_minutes) + ' min'

        # Préparation des valeurs pour le rendu
        valeurs = {
            'date': temps_ecoule,
            'id': derniere_ligne.id,
            'temp': derniere_ligne.temp,
            'hum': derniere_ligne.hum
        }
        return render(request, 'value.html', {'valeurs': valeurs})

    # Si aucune donnée n'est trouvée, renvoyer une réponse vide ou un message d'erreur
    return render(request, 'value.html', {'valeurs': None})


def download_csv(request):
    model_values = Dht11.objects.all()

    # Création de la réponse avec un type de contenu CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dht.csv"'

    # Initialisation du writer CSV
    writer = csv.writer(response)

    # Écriture de l'en-tête du fichier CSV
    writer.writerow(['id', 'temp', 'hum', 'dt'])

    # Extraction des valeurs de la base de données
    liste = model_values.values_list('id', 'temp', 'hum', 'dt')

    # Boucle pour écrire chaque ligne dans le fichier CSV
    for row in liste:
        writer.writerow(row)

    # Retour de la réponse CSV
    return response
