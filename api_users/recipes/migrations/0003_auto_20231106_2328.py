# Generated by Django 3.2.16 on 2023-11-06 19:28

from django.conf import settings
from django.db import migrations, models
import recipes.models
import recipes.validators


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20231106_2100'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favoritelist',
            options={'verbose_name': 'favorite recipe', 'verbose_name_plural': 'Favorite recipes'},
        ),
        migrations.AlterModelOptions(
            name='ingridient',
            options={'verbose_name': 'ingridient', 'verbose_name_plural': 'Ingridients'},
        ),
        migrations.AlterModelOptions(
            name='measurementunit',
            options={'verbose_name': 'measurement unit', 'verbose_name_plural': 'Measurement units'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'verbose_name': 'recipe', 'verbose_name_plural': 'Recipes'},
        ),
        migrations.AlterModelOptions(
            name='recipeingridient',
            options={'verbose_name': 'ingridient in recipe', 'verbose_name_plural': 'Ingridients in recipe'},
        ),
        migrations.AlterModelOptions(
            name='shoppingcart',
            options={'verbose_name': 'recipe in shopping cart', 'verbose_name_plural': 'Recipes in shopping cart'},
        ),
        migrations.AlterModelOptions(
            name='subscribe',
            options={'verbose_name': 'subscribe', 'verbose_name_plural': 'Subscribes'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'tag', 'verbose_name_plural': 'Tags'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'user', 'verbose_name_plural': 'Users'},
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.SmallIntegerField(default=1, validators=[recipes.validators.cooking_time_validator], verbose_name='cooking time'),
        ),
        migrations.AlterField(
            model_name='user',
            name='subscriptions',
            field=models.ManyToManyField(through='recipes.Subscribe', to=settings.AUTH_USER_MODEL, verbose_name='subscriptions'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=recipes.models.CharField150(default=recipes.validators.default_name, error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer.', max_length=150, unique=True, validators=[recipes.validators.username_validator], verbose_name='user name'),
        ),
    ]
