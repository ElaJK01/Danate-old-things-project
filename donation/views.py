from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from donation.forms import RegisterForm
from django.contrib.auth.models import User
from donation.models import CustomUser, Category, Institution, Donation
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import InstitutionSerializer, DonationSerializer, CategorySerializer
from rest_framework.generics import ListAPIView, CreateAPIView
from django.db.models import Sum
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.core import serializers


class LandingPage(View):
    def get(self, request):
        institutions_number = Institution.objects.all().count()
        institutions = Institution.objects.all()
        bags_number = Donation.objects.aggregate(Sum('quantity'))
        bags_number = bags_number['quantity__sum']
        categories = Category.objects.all()
        fundations = Institution.objects.filter(type=1)
        ngos = Institution.objects.filter(type=2)
        collections = Institution.objects.filter(type=3)
        ctx = {'institutions_number': institutions_number,
               'institutions': institutions,
               'bags_number': bags_number,
               'categories': categories,
               'fundations': fundations,
               'ngos': ngos,
               'collections': collections}
        return render(request, 'index.html', ctx)


class AddDonation(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'login'
    # response_data = {}

    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        ctx = {'categories': categories,
               'institutions': institutions}
        return render(request, 'form.html', ctx)

    def post(self, *args, **kwargs):
        if self.request.is_ajax() and self.request.method == "POST":
            user = self.request.user
            categories = self.request.POST.getlist('categories')
            bags = self.request.POST.get('bags')
            institution_pk = self.request.POST.get('organization')
            address = self.request.POST.get('address')
            city = self.request.POST.get('city')
            postcode = self.request.POST.get('postcode')
            phone = self.request.POST.get('phone')
            data = self.request.POST.get('data')
            time = self.request.POST.get('time')
            comments = self.request.POST.get('more_info')
            institution = Institution.objects.get(pk=institution_pk)
            if categories and bags and institution and address and city and postcode and phone and data and time \
                    and comments:

                donation = Donation.objects.create(quantity=bags, institution=institution, address=address,
                                                   phone_number=phone, city=city, zip_code=postcode, pick_up_date=data,
                                                   pick_up_time=time, pick_up_comment=comments, user=user)
                donation.categories.set(categories)
                donation.save()
                response = {
                    'msg': 'Formularz wysłany poprawnie! Dziękujemy!'  # response message
                }

                return JsonResponse(response)

            return render(self.request, 'form.html')




# class Donations(ListAPIView):
#     serializer_class = DonationSerializer
#     queryset = Donation.objects.all()
#
#
# class DonationAdd(CreateAPIView):
#     serializer_class = DonationSerializer
#     queryset = Donation.objects.all()


class Institutions(ListAPIView):
    serializer_class = InstitutionSerializer
    queryset = Institution.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('category', None)
        if category_id is not None:
            queryset = queryset.filter(categories__pk__in=[category_id])
        return queryset


class Login(LoginView):
    def form_invalid(self, form):
        return redirect('register')


class Register(View):
    def get(self, request):
        form = RegisterForm()
        ctx = {'form': form}
        return render(request, 'register.html', ctx)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            if password == password2:
                new_user = CustomUser.objects.create_user(email=email, name=name, last_name=last_name)
                new_user.set_password(password)
                new_user.save()
                return redirect('login')
        else:
            ctx = {'msg': "Niepoprawnie wypełniony formularz!"}
            return render(reqest, 'register.html', ctx)


class Profil(LoginRequiredMixin, View):
    def get(self, request):
        user = self.request.user
        ctx ={'user': user}
        return render(request, 'profil.html', ctx)

