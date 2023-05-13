from django.urls import path
#from .views import ShopView,HomeView,AboutView, CartView, DetailsView, BlogView,AccountsView
from . import views
from django.contrib.auth import views as auth_views




urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('blog/', views.BlogView.as_view(), name='blog'),
    path('blog/', views.BlogDetailView.as_view(), name='blogdetail'),
    path('shop/', views.ShopView.as_view(), name="shop"),
    path('about/', views.about, name="about"),
    path("add-to-cart/<slug>/", views.add_to_cart, name="add-to-cart"),
    path("remove-from-cart/<slug>/", views.remove_from_cart , name="remove-from-cart"),
    path("accounts/",views.accounts, name="accounts"),
    path('details/<slug>/', views.details, name="details"),
    path('Order_Summary/', views.OrderSummary.as_view(), name="order_summary"),
    path("remove-single-item-from-cart/<slug>/", views.remove_single_item_from_cart , name="remove-single-item-from-cart"),
    path('checkout/', views.CheckoutView.as_view(), name="checkout"),
    path('payment/<payment_option>', views.PaymentView.as_view(), name='payment'),
    path('coupon/<code>', views.add_coupon, name="coupon"),
    path('refund/', views.RequestRefundView.as_view(), name='refund')
    path('login/', views.login, name='login'),
    path('logout',LogoutView.as_view(next_page='login', template_name="registration/logout.html") , name='logout'),



]
