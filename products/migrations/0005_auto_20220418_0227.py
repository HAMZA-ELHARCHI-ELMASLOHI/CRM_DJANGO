# Generated by Django 3.1.14 on 2022-04-18 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20220418_0220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(default='images/products/product-default.png', upload_to='images/products/'),
        ),
    ]
