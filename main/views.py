from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from .models import *

class IndexView(View):
    def get(self, request):
        return render(request, 'index-unauth.html')

class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        banner_index = 1
        banners = Banner.objects.all()
        categories = Category.objects.all()
        context = {
            'banners': banners,
            'categories': categories
        }

        return render(request, 'index.html', context)


