"""GiveAway_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from donation.views import LandingPage, AddDonation, Register, Login, Institutions, Profil
from donation.forms import CustomAuthForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPage.as_view(), name='index'),
    path('add_donation/', AddDonation.as_view(), name='form'),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(authentication_form=CustomAuthForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('institutions/', Institutions.as_view()),
    path('profil/', Profil.as_view(), name='profil'),
    # path('donations/', Donations.as_view()),
    # path('donations/', DonationAdd.as_view()),

]
