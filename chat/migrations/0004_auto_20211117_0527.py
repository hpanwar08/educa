# Generated by Django 3.1.13 on 2021-11-17 05:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_auto_20211117_0429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='chat_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.chatgroup'),
        ),
    ]
