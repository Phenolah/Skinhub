from django.shortcuts import render
from .models import Item
from cloudinary.forms import cl_init_js_callbacks
from .forms import *

# Create your views here.
def home(request):
    return render(request, "skincare/main.html")
def blog(request):
    return render(request, "skincare/blog.html")
def shop(request):
    items = Item.objects.all()
    context = dict(items =items, backend_form = PhotoForm())
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        context['posted'] = form.instance
        if form.is_valid():
            form.save()
    return render(request, "skincare/shop.html", context)
def about(request):
    return render(request, "skincare/about.html")
def cart(request):
    return render(request, "skincare/cart.html")
def accounts(request):
    return render(request, "skincare/accounts.html")
"""def upload(request):
    context = dict( backend_form = PhotoForm)
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        context['posted'] = form.instance
        if form.is_valid():
            form.save()
    return render(request, 'shop.html', context)"""
