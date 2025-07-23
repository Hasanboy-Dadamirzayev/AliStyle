from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
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


class CategoryView(LoginRequiredMixin, View):
    def get(self, request, category_slug):
        category = get_object_or_404(Category, slug=category_slug)
        context = {
            'category': category
        }
        return render(request, 'category.html', context)


class SubCategoryView(LoginRequiredMixin, View):
    def get(self, request, category_slug, subcategory_slug):
        subcategory = get_object_or_404(SubCategory, slug=subcategory_slug)


        view = request.GET.get('view')
        context = {
            'subcategory': subcategory,
            'view': view
        }
        if view is not None:
            if view == 'large':
                return render(request, 'subcategory-large.html', context)
        return render(request, 'subcategory.html', context)


