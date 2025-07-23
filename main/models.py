from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify
from django.conf import settings

from core.settings import AUTH_USER_MODEL

User = settings.AUTH_USER_MODEL


class Category(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='image/', null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title)
            base_slug = slug

            count = 0
            while Category.objects.filter(slug=slug).exists():
                base_slug = slug + str(count)
                count += 1

            self.slug = base_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='image/', blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            count = 1
            while SubCategory.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Products(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    brand = models.CharField(max_length=255, blank=True, null=True)
    price = models.FloatField(validators=[MinValueValidator(0)])
    describtion = models.TextField(blank=True, null=True)
    guarantee = models.CharField(max_length=255, blank=True, null=True)
    delivery_time = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    rating = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    views = models.PositiveSmallIntegerField(default=0)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            base_slug = slug
            count = 0
            while Products.objects.filter(slug=slug).exists():
                base_slug = slug + str(count)
                count += 1

            self.slug = base_slug

        super().save(*args, **kwargs)


class Image(models.Model):
    image = models.ImageField(upload_to='image/', null=True, blank=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name


class Review(models.Model):
    comment = models.TextField(blank=True, null=True)
    rating = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name


class Discount(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    percentage = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    amount = models.PositiveSmallIntegerField(validators=[MinValueValidator(0)])
    end_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.percentage}"


class Banner(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='banners/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



