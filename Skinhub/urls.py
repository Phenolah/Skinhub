from django.urls import path
#from .views import ShopView,HomeView,AboutView, CartView, DetailsView, BlogView,AccountsView
from . import views
from django.contrib.auth import views as auth_views




urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('blog/', views.blog, name="blog"),
    path('shop/', views.ShopView.as_view(), name="shop"),
    path('about/', views.about, name="about"),
    path("add-to-cart/<slug>/", views.add_to_cart, name="add-to-cart"),
    path("remove-from-cart/<slug>/", views.remove_from_cart , name="remove-from-cart"),
    path("accounts/login/",views.accounts, name="accounts"),
    path('details/<slug>/', views.details, name="details"),
    path('Order_Summary/', views.OrderSummary.as_view(), name="order_summary"),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path("remove-single-item-from-cart/<slug>/", views.remove_single_item_from_cart , name="remove-single-item-from-cart"),
    path('checkout/', views.CheckoutView.as_view(), name="checkout"),
    path('payment/<payment_option>', views.PaymentView.as_view(), name='payment')


]