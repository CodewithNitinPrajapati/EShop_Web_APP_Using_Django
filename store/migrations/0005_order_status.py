# Generated by Django 3.1.6 on 2021-02-12 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
