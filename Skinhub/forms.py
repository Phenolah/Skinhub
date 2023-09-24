
from django.forms import ModelForm
from cloudinary.forms import CloudinaryJsFileField, CloudinaryUnsignedJsFileField
from cloudinary.compat import to_bytes
import cloudinary, hashlib
from django import forms
from django_countries.fields import CountryField
from .models import *
from django_countries.widgets import CountrySelectWidget
from django.core.validators import RegexValidator
from django.core import validators
class PhotoForm(ModelForm):
    class Meta:
        model = Item
        fields = "__all__"
        exclude = ['tittle', 'brief_description', 'price', 'size', 'product_description', 'number_of_Products']

class PhotoDirectForm(PhotoForm):
    image = CloudinaryJsFileField()

class PhotoUnsignedDirectForm(PhotoForm):
    upload_preset_name = "sample_" + hashlib.sha1(to_bytes(cloudinary.config().api_key + cloudinary.config().api_secret)).hexdigest()[0:10]
    image = CloudinaryUnsignedJsFileField(upload_preset_name)

PAYMENT_METHODS = [
    ('M', 'Mpesa'),
    ('D', 'Debit Card'),
    ('C', 'Credit Card'),
    ('P', 'Paypal'),

]

class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'House number and Street name',
        'type': 'text',
         'id': 'Street_address',
         'name': 'Street_address',
         'class': 'form-control'
    }))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Apartment/Suite (optional)',
        'type': 'text',
        'id': 'apartment_address',
        'name': 'apartment_address',
        'class': 'form-control'
    }))
    town = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Town/City',
        'type': 'text',
        'id': 'Town',
        'name': 'Town',
        'class': 'form-control'
    }))
    state = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'County/State',
        'type': 'text',
        'id': 'State',
        'name': 'State',
        'class': 'form-control'
    }))
    country = CountryField(blank_label='(Select Country)').formfield(
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100'
        })
    )
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Zip code',
        'type': 'text',
        'id': 'zip',
        'name': 'zip',
        'class': 'form-control'
    }))
    save_info = forms.BooleanField(widget=forms.CheckboxInput)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_METHODS, error_messages={'invalid_choice': 'Please select a valid payment option.'} )

    phone = forms.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$')], widget=forms.TextInput(attrs={
        'placeholder': 'Phonenumber',
        'type': 'tel',
         'id': 'phone',
        'name': 'phone',
        'class': 'form-control'
    }))
    #phone = forms.PhoneNumberField(help_text="Contact Phone Number", widget=forms.TextInput(attrs={
        #'placeholder': 'Phone Number',
        #'type': 'tel',
        #'id': 'phone',
        #'name':  'phone',
        #'class': 'form-control'
    #}))
    email = forms.EmailField( widget=forms.EmailInput(attrs={
        'placeholder': 'Email Address',
        'type': 'email',
        'id': 'email',
        'name': 'email',
        'class': 'form-control'
    }))
    class CouponForm(forms.Form):
             code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Discount Code',

                 }))

class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows' : 5,
        'class': 'form-control'

    }))
    email = forms.EmailField()











