# Generated by Django 3.2 on 2023-05-06 18:44

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0011_auto_20230506_2212'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ShopingCart',
            new_name='ShoppingCart',
        ),
    ]
