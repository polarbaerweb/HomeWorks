# Generated by Django 4.2 on 2023-05-09 13:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_listings_initialbids'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Bids',
        ),
    ]
