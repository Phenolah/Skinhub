from django.shortcuts import render, Http404, get_object_or_404
from .models import *
from .forms import *
from django.views.generic.list import ListView,View
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
import stripe
from stripe.error import APIConnectionError
import string
import random
from django.contrib.auth.forms import UserCreationForm
stripe.api_key = settings.STRIPE_TEST_KEY


# Create your views here.

def random_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

class HomeView(ListView):
    template_name = "skincare/main.html"
    context_object_name = 'items'
    success_url = reverse_lazy("add-to-cart")

    def get_queryset(self):
        return Item.objects.order_by('tittle')

def blog(request):
    return render(request, "skincare/blog.html")

class ShopView(ListView):
    context_object_name = 'items'
    paginate_by = 2
    def get(self, request, *args, **kwargs):
        items = Item.objects.all()
        paginator = Paginator(items, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = dict(items = page_obj, backend_form = PhotoForm(), page_obj=page_obj, paginator=paginator)
        if request.method == "POST":
            form = PhotoForm(request.POST, request.FILES)
            context['posted'] = form.instance
            if form.is_valid():
                form.save()
        return render(request, "skincare/shop.html", context)

def about(request):
    return render(request, "skincare/about.html")

@login_required(login_url='login')
class OrderSummary(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(customer=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request,'skincare/cart.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "Order does not exist")
            return redirect("/")

@login_required(login_url='login')
def add_to_cart(request,slug):
    item = Item.objects.get(slug=slug)
    order_item,created = OrderItem.objects.get_or_create(
        item=item,
        customer = request.user,
        ordered = False
    )
    order_qs = Order.objects.filter(customer=request.user, ordered=False)
    if order_qs.exists() :
        order = order_qs[0]
        if order.items.filter(item__slug = item.slug).exists():
            order_item.number_of_Products += 1
            order_item.save()
            messages.info(request, "This item quantity was updated")
            return redirect("order_summary")
        else:
            messages.info(request, "This item has been added to your cart")
            order.items.add(order_item)
            return redirect("order_summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(customer=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart")

    return redirect("details",slug=slug)

@login_required(login_url='login')
def remove_from_cart(request,slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        customer=request.user,
        ordered=False,
    )
    if order_qs.exists():
        order = order_qs[0]
        print("order_qs exists")
        if order.items.filter(item__slug=item.slug).exists():
            print("item exists in cart")
            order_item = OrderItem.objects.filter(
                item=item,
                customer=request.user,
                ordered = False,
            )[0]
            order.items.remove(order_item)
            messages.info(request, "Your item has been removed from the cart")
        else:
            messages.info(request, 'Item is not in your cart')
            return redirect("details", slug=slug)
    else:
        messages.info(request, 'You do not have an active order')
        return redirect("details", slug=slug)
    return redirect("details", slug=slug)

@login_required(login_url='login')
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    cart_qs = Order.objects.filter(
        customer=request.user,
        ordered = False,
    )
    if cart_qs.exists():
        cart = cart_qs[0]
        messages.info(request, "cart_qs exists")
        if cart.items.filter(item__slug=item.slug).exists():
            messages.info(request, "item exists in cart")
            cart_item = OrderItem.objects.filter(
                item=item,
                customer=request.user,
                ordered = False,
            )[0]
            cart_item.number_of_Products -= 1
            cart_item.save()
            messages.info(request, "item quantity has been decreased")
            return redirect('order_summary')
        else:
            messages.info(request, "item does not exist in cart")
            return redirect('order_summary')
    else:
        messages.info(request, "You have no active order")
        return redirect('order_summary')



def details(request, slug=None):
    items = None
    if slug is not None:
        try:
            items = Item.objects.filter(slug = slug)
        except:
            raise Http404
    context = {'items': items}
    template = "skincare/details.html"
    return render(request, template, context)

def accounts(request):
    context = {}
    if request.user.is_authenticated:
        return redirect ('home')
    else:
        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Hi {username}, your account has  been successfully created')
                return redirect('login')
        else:
            form = UserRegistrationForm()
            context = {
                'form': form
            }

        return render(request, "registration/accounts.html", context)

def login(request):
    form = UserRegistrationForm(request.POST)
    context = {
        'form': form
    }
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return redirect('home')
        return render(request, "registration/login.html", context)


def logout(request):
    return render(request, "registration/logout.html")


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(customer=self.request.user, ordered=False)
            form = CheckoutForm()
            Couponform = CouponForm()
            context = {
                'form': form,
                'order': order,
                'couponform' : Couponform
            }
            return render(self.request, 'skincare/checkout.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an order")
            return redirect("checkout")
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(customer=self.request.user, ordered=False)
            if form.is_valid():
                print(form.cleaned_data)
                payment_method = form.cleaned_data.get('payment_option')
                phone = form.cleaned_data.get('phone')
                email = form.cleaned_data.get('email')
                payment_option = form.cleaned_data.get('payment_option')


                order.save()
                messages.info(self.request, "Payment Submitted successfullly")
                if payment_option == 'M':
                    return redirect('payment', payment_option='Mpesa')
                elif payment_option == 'D':
                    return redirect('payment', payment_option='Debit card')
                elif payment_option == 'C':
                    return redirect('payment', payment_option='Credit card')
                elif payment_option == 'P':
                    return redirect('payment', payment_option='Paypal')
                else:
                    messages.warning(self.request, "Invalid payment option")
                    return redirect('checkout')
            else:
                for field in form:
                    for error in field.errors:
                        messages.warning(self.request, f"{field.label}: {error}")
                return redirect("checkout")
            if payment_option == 'M':
                return redirect('payment', payment_option='Mpesa')
            elif payment_option == 'D':
                return redirect('payment', payment_option='Debit card')
            elif payment_option == 'C':
                return redirect('payment', payment_option='Credit card')
            elif payment_option == 'P':
                return redirect('payment', payment_option='Paypal')
            else:
                messages.warning(self.request, "Invalid payment option")
                return redirect('checkout')

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("checkout")

@login_required(login_url='login')
class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(customer=self.request.user, ordered=False)
        form = CheckoutForm()
        Couponform = CouponForm()
        context = {
            'form': form,
            'order': order,
            'couponform': Couponform
        }

        return render(self.request, "skincare/payment.html", context)
    def post(self, *args, **kwargs):
        order = Order.objects.get(customer=self.request.user, ordered=False)
        token = self.request.POST.get("StripeToken")
        amount = int(order.get_total() * 12500)
        try:
            charge = stripe.Charge.create(
                amount = amount,
                currency = "Kshs",
                source = token,
                description = "phenolaha@gmail.com"
            )
            # create payment
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.customer = self.request.user
            payment.amount = order.get_total()
            payment.save()

            # assign payment to the order
            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()

            order.ordered = True
            order.payment = payment
            order.ref_code = random_ref_code()
            order.save()
            messages.success(self.request, "Your order was successful")
            return redirect("/")
        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.error(self.request, f'{err.get("message")}')
            return redirect("/")
        except stripe.error.RateLimitError as e:
            # too many requests made to the API too quickly
            messages.error(self.request, "Rate Limit error")
            return redirect("/")
        except stripe.error.InvalidRequestError as e:
            # invalid parameters were supplied to Stripe API
            messages.error(self.request, "Invalid parameter")
            return redirect("/")
        except stripe.error.AuthenticationError as e:
            #authentication with Stripes API failed
            #maybe you  changed API keys
            messages.error(self.request, "Not Authenticated")
            return redirect("/")
        except stripe.error.APIConnectError as e:
            # network communication with stripe :failed
            messages.error(self.request, "Network error")
            return redirect("/")
        except stripe.error.StripeError as e:
            #Display a very generic error to the user and maybe send yourself an email
            messages.error(self.request," Something went wrong. You were not charged. Please try again")
            return redirect("/")
        except Exception as e:
            #send an email to ourselves
            messages.error(self.request, "A serious error occurred. We have been notified")
            return redirect("/")
        
@login_required(login_url='login')        
def get_coupon(request, code):
    try:
        coupon = DiscountCode.objects.get(code=code)

        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("checkout")

@login_required(login_url='login')
class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(customer=self.request.user, ordered=False)
                order.discount_coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, 'Successfully added coupon')
                return redirect('checkout')
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect('checkout')
            
@login_required(login_url='login')
class RequestRefundView(View):
    def get(self, *arg, **kwargs):
        form = RefundForm
        context = {
            'form': form
        }

        return render(self.request, 'skincare/refund.html', context)
    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()
                messages.info(self.request, 'Your request has been received')
                return redirect('home')

            except ObjectDoesNotExist:
                message.info(self.request, 'Order doesn\'t exist')
                return redirect('home')



