from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout

from order.models import Order
from .models import *
from random import randint


email = 'dadamirzayevhasanboy5@gmail.com'
password = 'UKK4HbFWHxyhW6o8g66XaS2eOW2yOLprBSvLp9fa'






class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        if request.POST.get('password1') == request.POST.get('password2'):
            user = authenticate(
                username=request.POST.get('username'),
                password=request.POST.get('password')
            )
            if user is not None:
                return self.get(request)
            user = User.objects.create_user(
                username=request.POST.get('phone'),
                phone_number=request.POST.get('phone'),
                password=request.POST.get('password1'),
                gender=request.POST.get('gender'),
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                city=request.POST.get('city'),
                country=request.POST.get('country'),
            )

            confirmation_code = randint(100000, 999999)
            print(confirmation_code)
            user.confirmation_code=confirmation_code
            user.save()
            login(request, user)
            return redirect('register-confirm')
        else:
            return self.get(request)

class RegisterConfirmView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'register_confirm.html')
        return redirect('index')

    def post(self, request):
        if request.user.is_authenticated:
            confirmation_code = request.POST.get('confirmation_code')
            user=request.user

            if user.confirmation_code==confirmation_code:
                user.confirmed = True
                user.save()
                return redirect('home')
            return self.get(request)
        return redirect('index')

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        user = authenticate(
            username=request.POST.get('phone_number'),
            password=request.POST.get('password')
        )

        if user is not None:
            login(request, user)
            return redirect('home')
        return self.get(request)


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user

        awating_orders = user.order_set.exclude(status=Order.STATUS_CHOICES[3][0]).count()

        order_items = 0

        for order in user.order_set.all():
            order_items += order.orderitem_set.count()

        context = {
            'user': user,
            'awating_orders': awating_orders,
            'order_items': order_items
        }
        return render(request, 'profile-main.html', context)


class ProfileSettingsView(LoginRequiredMixin, View):
    def get(self, request):

        user = request.user
        context = {
            'user': user
        }

        return render(request, 'profile-settings.html', context)

    def post(self, request):
        user = request.user

        user.first_name=request.POST.get('first_name')
        user.last_name=request.POST.get('last_name')
        user.country=request.POST.get('country')
        user.city=request.POST.get('city')
        user.phone_number=request.POST.get('phone_number')
        user.username=request.POST.get('phone_number')
        user.save()

        return redirect('profile-settings')

def logout_view(request):
    logout(request)
    return redirect('home')


