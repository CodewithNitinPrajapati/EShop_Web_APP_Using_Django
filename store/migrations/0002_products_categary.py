# Generated by Django 3.1.6 on 2021-02-05 05:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='categary',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='store.categary'),
        ),
    ]
