from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('blog/', views.blog, name="blog"),
    path('shop/', views.shop, name="shop"),
    path('about/', views.about, name="about"),
    path("cart/", views.cart, name="cart"),
    path("accounts/", views.accounts, name="accounts"),
]