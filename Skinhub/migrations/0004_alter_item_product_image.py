# Generated by Django 4.0.5 on 2022-09-09 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Skinhub', '0003_alter_item_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='product_image',
            field=models.ImageField(default='', upload_to='static/image'),
        ),
    ]
