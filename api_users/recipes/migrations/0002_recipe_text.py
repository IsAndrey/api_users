# Generated by Django 3.2.16 on 2023-09-30 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='text',
            field=models.TextField(default='', max_length=200),
        ),
    ]