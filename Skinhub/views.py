from django.shortcuts import render, Http404, get_object_or_404
from .models import *
from .forms import *
from django.views.generic.list import ListView, View
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
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.contrib.auth.forms import UserCreationForm

stripe.api_key = settings.STRIPE_TEST_KEY

# Utility function to generate a random reference code
def random_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

# HomeView is a class-based view that extends the ListView class
class HomeView(ListView):
    template_name = "skincare/main.html"
    context_object_name = 'items'
    success_url = reverse_lazy("add-to-cart")

    def get_queryset(self):
        return Item.objects.order_by('tittle')

# BlogView is a class-based view that extends the ListView class
class BlogView(generic.ListView):
    model = Blog
    template_name ='skincare/blog.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

# BlogDetailView is a class-based view that extends the DetailView class
class BlogDetailView(generic.DetailView):
    model = Blog
    template_name = 'skincare/blogdetail.html'
    context_object_name = 'blogs'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        blogs = Blog.objects.get(slug=slug)
        return blogs


class ShopView(ListView):
    # The name of the variable to use in the template to access the list of items
    context_object_name = 'items'
    # The number of items to display per page
    paginate_by = 2

    def get(self, request, *args, **kwargs):
        # Retrieve all items from the database
        items = Item.objects.all()
        # Create a paginator object with the items and the specified number of items per page
        paginator = Paginator(items, self.paginate_by)
        # Get the page number from the request's GET parameters
        page_number = request.GET.get('page')
        # Get the page object for the specified page number
        page_obj = paginator.get_page(page_number)
        # Create a context dictionary with the page object, a form object, and other variables
        context = dict(items=page_obj, backend_form=PhotoForm(), page_obj=page_obj, paginator=paginator)
        
        if request.method == "POST":
            # Create a form object with the POST data
            form = PhotoForm(request.POST, request.FILES)
            # Add the form instance to the context dictionary
            context['posted'] = form.instance
            if form.is_valid():
                # Save the form data to the database
                form.save()
        
        # Render the template with the context dictionary
        return render(request, "skincare/shop.html", context)


def about(request):
    # Render the "about" template
    return render(request, "skincare/about.html")


class OrderSummary(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            # Get the order for the current user that is not yet ordered
            order = Order.objects.get(customer=self.request.user, ordered=False)
            context = {
                'object': order
            }
            # Render the "cart" template with the order object in the context
            return render(self.request, 'skincare/cart.html', context)
        except ObjectDoesNotExist:
            # If the order does not exist, display an error message and redirect to the homepage
            messages.error(self.request, "Order does not exist")
            return redirect("/")


@login_required
def add_to_cart(request, slug):
    item = Item.objects.get(slug=slug)
    # Get or create an order item for the item and the current user
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        customer=request.user,
        ordered=False
    )
    # Get the active order for the current user
    order_qs = Order.objects.filter(customer=request.user, ordered=False)
    if order_qs.exists():
        # If the order exists, get the first order from the queryset
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            # If the item is already in the order, increase the quantity and save the order item
            order_item.number_of_Products += 1
            order_item.save()
            messages.info(request, "This item quantity was updated")
            return redirect("order_summary")
        else:
            # If the item is not in the order, add it to the order
            messages.info(request, "This item has been added to your cart")
            order.items.add(order_item)
            return redirect("order_summary")
    else:
        # If no active order exists, create a new order and add the item to it
        ordered_date = timezone.now()
        order = Order.objects.create(customer=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart")

    return redirect("details",slug=slug)
@login_required
def remove_from_cart(request, slug):
    # Get the item with the specified slug from the database
    item = get_object_or_404(Item, slug=slug)
    # Filter the orders to find the active order for the current user
    order_qs = Order.objects.filter(
        customer=request.user,
        ordered=False,
    )
    if order_qs.exists():
        # If an active order exists, get the first order from the queryset
        order = order_qs[0]
        print("order_qs exists")
        if order.items.filter(item__slug=item.slug).exists():
            # If the item exists in the order, remove it from the order
            print("item exists in cart")
            order_item = OrderItem.objects.filter(
                item=item,
                customer=request.user,
                ordered=False,
            )[0]
            order.items.remove(order_item)
            messages.info(request, "Your item has been removed from the cart")
        else:
            # If the item is not in the order, display a message and redirect to the item's details page
            messages.info(request, 'Item is not in your cart')
            return redirect("details", slug=slug)
    else:
        # If no active order exists, display a message and redirect to the item's details page
        messages.info(request, 'You do not have an active order')
        return redirect("details", slug=slug)
    # Redirect to the item's details page
    return redirect("details", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    # Get the item with the specified slug from the database
    item = get_object_or_404(Item, slug=slug)
    # Filter the orders to find the cart for the current user
    cart_qs = Order.objects.filter(
        customer=request.user,
        ordered=False,
    )
    if cart_qs.exists():
        # If a cart exists, get the first cart from the queryset
        cart = cart_qs[0]
        messages.info(request, "cart_qs exists")
        if cart.items.filter(item__slug=item.slug).exists():
            # If the item exists in the cart, decrease the quantity of the item by 1
            messages.info(request, "item exists in cart")
            cart_item = OrderItem.objects.filter(
                item=item,
                customer=request.user,
                ordered=False,
            )[0]
            cart_item.number_of_Products -= 1
            cart_item.save()
            messages.info(request, "item quantity has been decreased")
            return redirect('order_summary')
        else:
            # If the item is not in the cart, display a message and redirect to the order summary page
            messages.info(request, "item does not exist in cart")
            return redirect('order_summary')
    else:
        # If no cart exists, display a message and redirect to the order summary page
        messages.info(request, "You have no active order")
        return redirect('order_summary')


def details(request, slug=None):
    items = None
    if slug is not None:
        try:
            # Filter the items to find the items with the specified slug
            items = Item.objects.filter(slug=slug)
        except:
            raise Http404
    context = {'items': items}
    template = "skincare/details.html"
    return render(request, template, context)


def accounts(request):
    context = {}
    if request.user.is_authenticated:
        # If the user is already authenticated, redirect to the home page
        return redirect('home')
    else:
        if request.method == 'POST':
            # If the request method is POST, create a user
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
                        
def loginView(request):
    form = UserLoginForm(request.POST)
    context = {
        'form': form
    }
    if request.user.is_authenticated:
        # If the user is already authenticated, redirect to the home page
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # If the user credentials are valid, log in the user and redirect to the home page
                login(request, user)
                return redirect('home')
            else:
                # If the user credentials are invalid, redirect to the home page
                return redirect('home')
        # Render the login form
        return render(request, "registration/login.html", context)


def logout(request):
    # Render the logout page
    return render(request, "registration/logout.html")


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            # Get the active order for the current user
            order = Order.objects.get(customer=self.request.user, ordered=False)
            form = CheckoutForm()
            Couponform = CouponForm()
            context = {
                'form': form,
                'order': order,
                'couponform': Couponform
            }
            # Render the checkout page with the order details and checkout form
            return render(self.request, 'skincare/checkout.html', context)
        except ObjectDoesNotExist:
            # If no active order exists for the user, display a message and redirect to the checkout page
            messages.info(self.request, "You do not have an order")
            return redirect("checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            # Get the active order for the current user
            order = Order.objects.get(customer=self.request.user, ordered=False)
            if form.is_valid():
                # If the checkout form is valid, process the payment and redirect to the appropriate payment page
                print(form.cleaned_data)
                payment_method = form.cleaned_data.get('payment_option')
                phone = form.cleaned_data.get('phone')
                email = form.cleaned_data.get('email')
                payment_option = form.cleaned_data.get('payment_option')

                order.save()
                messages.info(self.request, "Payment Submitted successfully")
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
                # If the form is invalid, display form errors and redirect to the checkout page
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
class PaymentView(View):
    def get(self, *args, **kwargs):
        # Get the active order for the current user
        order = Order.objects.get(customer=self.request.user, ordered=False)
        form = CheckoutForm()
        Couponform = CouponForm()
        context = {
            'form': form,
            'order': order,
            'couponform': Couponform
        }
        # Render the payment page with the order details and checkout form
        return render(self.request, "skincare/payment.html", context)

    def post(self, *args, **kwargs):
        # Get the active order for the current user
        order = Order.objects.get(customer=self.request.user, ordered=False)
        token = self.request.POST.get("StripeToken")
        amount = int(order.get_total() * 12500)
        try:
            # Create a charge using the Stripe API
            charge = stripe.Charge.create(
                amount=amount,
                currency="Kshs",
                source=token,
                description="phenolaha@gmail.com"
            )

            # Create a payment record
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.customer = self.request.user
            payment.amount = order.get_total()
            payment.save()

            # Mark order items as ordered
            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()

            # Update order details
            order.ordered = True
            order.payment = payment
            order.ref_code = random_ref_code()
            order.save()

            messages.success(self.request, "Your order was successful")
            return redirect("/")
        except stripe.error.CardError as e:
            # Handle specific error: CardError
            body = e.json_body
            err = body.get('error', {})
            messages.error(self.request, f'{err.get("message")}')
            return redirect("/")
        except stripe.error.RateLimitError as e:
            # Handle specific error: RateLimitError
            messages.error(self.request, "Rate Limit error")
            return redirect("/")
        except stripe.error.InvalidRequestError as e:
            # Handle specific error: InvalidRequestError
            messages.error(self.request, "Invalid parameter")
            return redirect("/")
        except stripe.error.AuthenticationError as e:
            # Handle specific error: AuthenticationError
            messages.error(self.request, "Not Authenticated")
            return redirect("/")
        except stripe.error.APIConnectError as e:
            # Handle specific error: APIConnectError
            messages.error(self.request, "Network error")
            return redirect("/")
        except stripe.error.StripeError as e:
            # Handle generic Stripe error
            messages.error(self.request,"Something went wrong. You were not charged. Please try again")
            return redirect("/")
        except Exception as e:
            # Handle other exceptions
            messages.error(self.request, "A serious error occurred. We have been notified")
            return redirect("/")
def get_coupon(request, code):
    try:
        # Get the discount code object based on the provided code
        coupon = DiscountCode.objects.get(code=code)

        return coupon
    except ObjectDoesNotExist:
        # Handle the case when the coupon does not exist
        messages.info(request, "This coupon does not exist")
        return redirect("checkout")

class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                # Get the code from the form
                code = form.cleaned_data.get('code')
                # Get the active order for the current user
                order = Order.objects.get(customer=self.request.user, ordered=False)
                # Assign the discount coupon to the order
                order.discount_coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, 'Successfully added coupon')
                return redirect('checkout')
            except ObjectDoesNotExist:
                # Handle the case when the user does not have an active order
                messages.info(self.request, "You do not have an active order")
                return redirect('checkout')
class RequestRefundView(View):
    def get(self, *arg, **kwargs):
        # Create an instance of the RefundForm
        form = RefundForm
        context = {
            'form': form
        }

        return render(self.request, 'skincare/refund.html', context)

    def post(self, *args, **kwargs):
        # Create an instance of the RefundForm with the submitted data
        form = RefundForm(self.request.POST)
        if form.is_valid():
            # Get the refund code, message, and email from the form
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            try:
                # Get the order based on the refund code
                order = Order.objects.get(ref_code=ref_code)
                # Mark the order as refund requested
                order.refund_requested = True
                order.save()

                # Create a refund object and associate it with the order
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()
                messages.info(self.request, 'Your request has been received')
                return redirect('home')

            except ObjectDoesNotExist:
                # Handle the case when the order does not exist
                message.info(self.request, 'Order doesn\'t exist')
                return redirect('home')
        
