# Generated by Django 3.2.9 on 2021-11-11 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='group_name',
            field=models.CharField(max_length=100),
        ),
    ]
