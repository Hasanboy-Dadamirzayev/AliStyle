from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .models import *
from random import randint
from eskiz_sms import EskizSMS

email = 'dadamirzayevhasanboy5@gmail.com'
password = 'UKK4HbFWHxyhW6o8g66XaS2eOW2yOLprBSvLp9fa'

eskiz = EskizSMS(email, password)




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
            eskiz.send_sms(user.phone_number, 'Bu eskiz dan test')
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

