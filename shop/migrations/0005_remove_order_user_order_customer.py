# Generated by Django 4.0.3 on 2022-05-05 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0010_manager'),
        ('shop', '0004_alter_orderitems_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='order_user', to='Dashboard.customer'),
        ),
    ]
