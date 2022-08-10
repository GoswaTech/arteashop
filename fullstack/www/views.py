from django.shortcuts import render

from .finder import Finder


# Create your views here.
def index(request):

    message = 'Résultat de la recherche d\'articles :\n'

    library = {}

    # Init Finder
    finder = Finder()

    # Récupère les catégories dans le dossier products
    categories = finder.find_categories()

    # Récupère les articles de chaque catégorie
    for category in categories:
        library.append(finder.find_articles(category))

    # Ajoute un message
    for category in categories:
        message += category+' / '

    message += '.. / .'

    context = {
        'site_title': 'Artea Shop',
        'message': message,
    }

    return render(request, 'www/index.html', context)
