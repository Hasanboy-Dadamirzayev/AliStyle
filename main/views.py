from django.shortcuts import render, redirect
from django.views import View

class IndexView(View):
    def get(self, request):
        return render(request, 'index-unauth.html')

class HomeView(View):
    def get(self, request):
        return render(request, 'index.html')


