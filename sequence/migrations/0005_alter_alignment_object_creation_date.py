# Generated by Django 4.0.2 on 2022-03-10 14:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sequence', '0004_alignment_object_creation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alignment',
            name='object_creation_date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='Key as date-time field'),
        ),
    ]
