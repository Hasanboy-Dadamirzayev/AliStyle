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
        products = Products.objects.filter(sub_category=subcategory).order_by('rating')

        countries = products.values_list('country', flat=True).distinct()
        brands = products.values_list('brand', flat=True).distinct()

        # Filters from GET
        min_price = request.GET.get('min_price') or None
        max_price = request.GET.get('max_price') or None
        filter_countries = request.GET.getlist('country')
        filter_brands = request.GET.getlist('brand')

        # Apply filters
        if filter_countries:
            products = products.filter(country__in=filter_countries)
        if filter_brands:
            products = products.filter(brand__in=filter_brands)
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)

        view = request.GET.get('view')

        context = {
            'subcategory': subcategory,
            'products': products,
            'countries': countries,
            'brands': brands,
            'filter_countries': filter_countries,
            'filter_brands': filter_brands,
            'min_price': min_price,
            'max_price': max_price,
            'view': view,
        }

        if view == 'large':
            return render(request, 'subcategory-large.html', context)

        return render(request, 'subcategory.html', context)


class ProductView(LoginRequiredMixin, View):
    def get(self, request, slug):
        product = get_object_or_404(Products, slug=slug)

        context = {
            'product': product
        }
        return render(request, 'product-info.html', context)
