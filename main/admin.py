from django.contrib import admin
from .models import *

from django.contrib import admin
from .models import Products, SubCategory, Category


admin.site.register(Banner)


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}



admin.site.register(Review)
admin.site.register(Image)
admin.site.register(Discount)
admin.site.register(Favorite)


