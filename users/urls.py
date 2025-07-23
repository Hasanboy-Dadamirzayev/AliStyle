from django.urls import path
from .views import *



urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('register-confirm/', RegisterConfirmView.as_view(), name='register-confirm'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout')
]

urlpatterns += [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile-settings/', ProfileSettingsView.as_view(), name='profile-settings')
]