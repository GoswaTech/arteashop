from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .finder import Finder
from .forms import LoginForm


# Create your views here.
def index(request, **kwargs):

    library = {}

    # Init Finder
    finder = Finder()

    # Récupère les catégories dans le dossier products
    categories = finder.find_categories()

    # Récupère les articles de chaque catégorie
    for category in categories:
        articles = finder.find_articles(category=category.lower())
        library[category.lower()] = articles.get(category.lower(), [])

    context = {
        'site_title': 'Artea Shop',
        'library': library,
        'private': False,
    }

    return render(request, 'www/pages/home.html', context)


def private(request):
    library = {}

    # Init Finder
    finder = Finder(productsdir='private_products')

    # Récupère les catégories dans le dossier products
    categories = finder.find_categories()

    # Récupère les articles de chaque catégorie
    for category in categories:
        articles = finder.find_articles(category=category.lower())
        library[category.lower()] = articles.get(category.lower(), [])

    context = {
        'site_title': 'Artea Private Shop',
        'library': library,
        'private': True,
    }

    return render(request, 'www/pages/home.html', context)


def login_view(request, slug):

    user = None
    is_authenticated = request.user.is_authenticated
    form = LoginForm()

    context = {
        'slug': slug,
        'user': user,
        'is_authenticated': is_authenticated,
        'form': form,
    }

    if is_authenticated:
        return redirect('private')

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.pop('username', slug)
            password = form.cleaned_data.pop('password', '')
            print(username, password)
            user = authenticate(username=username, password=password)
            print('AUTHENTICATE')
            if user is not None:
                context['is_authenticated'] = True
                context['user'] = user
                login(request, user)
                return redirect('private')
            else:
                print('ELSE')

    return render(request, 'www/pages/private_login.html', context)


def logout_view(request):
    logout(request)
    return redirect('index')


def contact(request):
    return redirect('index')
