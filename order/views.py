from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import request
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *


class OrderView(LoginRequiredMixin, View):
    def get(self, request):
        cart_items = request.user.cartitem_set.all()
        wishlist_products = request.user.favorite_set.values_list('product__id', flat=True)

        context = {
            'cart_items': cart_items,
            'wishlist_products': wishlist_products
        }
        return render(request, 'order.html', context)


class AddToCart(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = get_object_or_404(Products, id=product_id)
        cart_items = CartItem.objects.filter(
            product=product,
            user=request.user
        )
        if cart_items.exists():
            cart_item = cart_items.first()
            cart_item.amount += 1
            cart_item.save()
            return redirect('my-cart')


        CartItem.objects.create(
            product=get_object_or_404(Products, id=product_id),
            user=request.user
        )
        return redirect('my-cart')

class RemoveFromCart(LoginRequiredMixin, View):
    def get(self, request, product_id):
        CartItem.objects.filter(
            product=get_object_or_404(Products, id=product_id),
            user=request.user
        ).delete()
        return redirect('my-cart')


def cart_item_inc(request, cart_item_id):
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, id=cart_item_id)
        cart_item.amount += 1
        cart_item.save()
        return redirect('my-cart')
    return redirect('login')

def cart_item_dec(request, cart_item_id):
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, id=cart_item_id)
        if cart_item.amount == 1:
            cart_item.delete()
            return redirect('my-cart')
        cart_item.amount -= 1
        cart_item.save()
        return redirect('my-cart')
    return redirect('login')