from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class OrderView(LoginRequiredMixin, View):
    def get(self, request):
        cart_items = request.user.cartitem_set.all()

        context = {
            'cart_items': cart_items
        }
        return render(request, 'order.html', context)



