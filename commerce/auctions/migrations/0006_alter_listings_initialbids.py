# Generated by Django 4.2 on 2023-05-09 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_bids_comments_remove_listings_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='initialBids',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='auctions.bids'),
        ),
    ]
