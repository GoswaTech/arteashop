from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/<str:slug>/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('private/', views.private, name='private'),
    path('contact/', views.contact, name='contact'),
]
