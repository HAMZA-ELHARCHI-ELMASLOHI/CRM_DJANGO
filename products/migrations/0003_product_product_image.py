# Generated by Django 3.1.14 on 2022-04-18 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20220418_0130'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_image',
            field=models.ImageField(default='images/products/product-default.png', upload_to='images/products/'),
        ),
    ]
