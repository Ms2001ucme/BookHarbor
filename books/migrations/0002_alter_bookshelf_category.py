# Generated by Django 5.1.4 on 2025-03-09 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookshelf',
            name='category',
            field=models.CharField(choices=[('to_read', 'To Read'), ('favorites', 'Favorites'), ('lent_out', 'Lent Out'), ('watchlist', 'Watchlist')], default='to_read', max_length=20),
        ),
    ]
