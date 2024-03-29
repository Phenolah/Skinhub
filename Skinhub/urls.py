from django.urls import path
#from .views import ShopView,HomeView,AboutView, CartView, DetailsView, BlogView,AccountsView
from . import views
from django.contrib.auth import views as auth_views




urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('blog/', views.BlogView.as_view(), name='blog'),
    path('blogdetail/<slug:slug>/', views.BlogDetailView.as_view(), name='blogdetail'),
    path('shop/', views.ShopView.as_view(), name="shop"),
    path('details/<slug>/', views.details, name="details"),
    path('about/', views.about, name="about"),
    path("add-to-cart/<slug>/", views.add_to_cart, name="add-to-cart"),
    path("remove-from-cart/<slug>/", views.remove_from_cart , name="remove-from-cart"),
    path("accounts/",views.accounts, name="accounts"),
    path('login/', views.loginView, name='login'),
    path('logout',auth_views.LogoutView.as_view(next_page='login', template_name="registration/logout.html") , name='logout'),
    path('Order_Summary/', views.OrderSummary.as_view(), name="order_summary"),
    path("remove-single-item-from-cart/<slug>/", views.remove_single_item_from_cart , name="remove-single-item-from-cart"),
    path('checkout/', views.CheckoutView.as_view(), name="checkout"),
    path('payment/<payment_option>', views.PaymentView.as_view(), name='payment'),
    path('coupon/<code>', views.AddCouponView.as_view(), name="coupon"),
    path('refund/', views.RequestRefundView.as_view(), name='refund'),



]
