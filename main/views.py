from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import *
from django.shortcuts import render, get_object_or_404, redirect
from .models import Products, Review
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import logout



class IndexView(View):
    def get(self, request):
        banner_index = 1
        banners = Banner.objects.all()
        categories = Category.objects.all()
        products = Products.objects.all()
        context = {
            'banners': banners,
            'categories': categories,
            'products': products
        }
        return render(request, 'index-unauth.html', context)

class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        banner_index = 1
        banners = Banner.objects.all()
        categories = Category.objects.all()
        products = Products.objects.all()
        context = {
            'banners': banners,
            'categories': categories,
            'products': products
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

        paginator = Paginator(products, 1)
        page_number = request.GET.get('page')

        products_page = paginator.get_page(page_number)  # bu yerda .get_page() o‘zi noto‘g‘rilarni to‘g‘rilaydi

        pages = range(1, paginator.num_pages + 1)

        context = {
            'subcategory': subcategory,
            'products': products_page,
            'countries': countries,
            'brands': brands,
            'filter_countries': filter_countries,
            'filter_brands': filter_brands,
            'min_price': min_price,
            'max_price': max_price,
            'view': view,
            'pages': pages,
            'page': products_page.number,
            'pr_page': products_page.number - 1 if products_page.number > 1 else 1,
            'nt_page': products_page.number + 1 if products_page.number < paginator.num_pages else paginator.num_pages
        }

        if view == 'large':
            return render(request, 'subcategory-large.html', context)

        return render(request, 'subcategory.html', context)



@login_required
def product_detail(request, slug):
    product = get_object_or_404(Products, slug=slug)
    reviews = Review.objects.filter(product=product)

    # GET dan main_image ni olish
    main_image_id = request.GET.get('main_image')
    if main_image_id:
        try:
            main_image = Image.objects.get(id=main_image_id, product=product)
        except Image.DoesNotExist:
            main_image = product.images.first()
    else:
        main_image = product.images.first()

    # POST so‘rovni qayta ishlash (rating + comment)
    if request.method == 'POST':
        rating = int(request.POST.get('rating', 0))
        comment = request.POST.get('comment', '')

        if rating:
            Review.objects.update_or_create(
                product=product,
                user=request.user,
                defaults={
                    'rating': rating,
                    'comment': comment,
                }
            )
        return redirect('product', slug=product.slug)  # URL nomi 'product' bo‘lishi kerak

    average_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0

    return render(request, 'product-info.html', {
        'product': product,
        'izohlar': reviews,
        'average_rating': average_rating,
        'main_image': main_image,
    })


class WishListView(LoginRequiredMixin, View):
    def get(self, request):
        favorites = Favorite.objects.filter(user=request.user)
        context = {
            'favorites': favorites
        }
        return render(request, 'wishlist.html', context)

class AddToWishlistView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = get_object_or_404(Products, id=product_id)
        Favorite.objects.create(
            user=request.user,
            product=product
        )
        return redirect('wishlist')


class RemoveFromWishlistView(LoginRequiredMixin, View):
    def get(self, request, favorite_id):
        favorite = get_object_or_404(Favorite, id=favorite_id)
        favorite.delete()
        return redirect('wishlist')


class AddToWishlistForCartView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = get_object_or_404(Products, id=product_id)

        favorites = Favorite.objects.filter(user=request.user, product=product)
        if favorites.exists():
            favorites.delete()
        else:
            Favorite.objects.create(
                user=request.user,
                product=product
            )
        return redirect('my-cart')

def logout_view(request):
    logout(request)
    return redirect('index')
