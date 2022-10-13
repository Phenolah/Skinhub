from django.forms import ModelForm
from .models import Item
from cloudinary.forms import CloudinaryJsFileField, CloudinaryUnsignedJsFileField
from cloudinary.compat import to_bytes
import cloudinary, hashlib

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
