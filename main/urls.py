from django.urls import path
from .views import *


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('home/', HomeView.as_view(), name='home'),
    path('category/<category_slug>/', CategoryView.as_view(), name='category'),
    path('category/<category_slug>/<subcategory_slug>/', SubCategoryView.as_view(), name='sub-category'),
    path('product/<slug:slug>/', product_detail, name='product'),
    path('my-wishlist/', WishListView.as_view(), name='wishlist'),
    path('add-to-wishlist/<int:product_id>/', AddToWishlistView.as_view(), name='add-to-wishlist'),
    path('add-to-wishlist-for-cart/<int:product_id>/', AddToWishlistForCartView.as_view(), name='add-to-wishlist-for-cart'),
    path('remove-from-wishlist/<int:favorite_id>/', RemoveFromWishlistView.as_view(), name='remove-from-wishlist'),
]