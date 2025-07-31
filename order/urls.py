from django.urls import path


from .views import *

urlpatterns = [
    path('my-cart/', OrderView.as_view(), name='my-cart'),
    path('my-cart/<int:cart_item_id>/increment/', cart_item_inc, name='increment'),
    path('my-cart/<int:cart_item_id>/decrement/', cart_item_dec, name='decrement'),
    path('add-to-cart/<int:product_id>/', AddToCart.as_view(), name='add-to-cart'),
    path('remove-from-cart/<int:product_id>/', RemoveFromCart.as_view(), name='remove-from-cart'),
]