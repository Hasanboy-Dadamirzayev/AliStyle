from django.urls import path
from .views import *


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('home/', HomeView.as_view(), name='home'),
    path('category/<category_slug>/', CategoryView.as_view(), name='category'),
    path('category/<category_slug>/<subcategory_slug>/', SubCategoryView.as_view(), name='sub-category'),
    path('product/<slug:slug>/', product_detail, name='product'),

]