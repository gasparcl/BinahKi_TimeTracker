"""TimeTracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

# Importando as views
from apps.core.views import *
from apps.userprofile.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', frontpage, name='frontpage'),
    path('politica-privacidade/', privacidade, name='privacidade'),
    path('termos-de-uso/', termos, name='termos'),

    # Dashboard
    path('dashboard/', include('apps.dashboard.urls')),       

    # Autenticação
    path('cadastro/', cadastro, name='cadastro'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    # Não há necessidade de um template_name, pois como padrão do Django, o LogoutView() redireciona o usuário para homepage 
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]
