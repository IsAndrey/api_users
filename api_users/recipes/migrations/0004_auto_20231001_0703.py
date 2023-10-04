# Generated by Django 3.2.16 on 2023-10-01 03:03

from django.db import migrations, models
import django.db.models.deletion
import recipes.validators


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_recipe_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingridient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=200)),
                ('measurement_unit', models.TextField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('color', models.TextField(max_length=7)),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='cooking_time',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='recipe',
            name='image',
            field=models.URLField(default=recipes.validators.default_recipe_image),
        ),
        migrations.AddField(
            model_name='recipe',
            name='name',
            field=models.TextField(default='', max_length=200),
        ),
        migrations.CreateModel(
            name='RecipeIngridient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingridient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingridients', to='recipes.ingridient')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to='recipes.recipe')),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingridients',
            field=models.ManyToManyField(through='recipes.RecipeIngridient', to='recipes.Ingridient'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(to='recipes.Tag'),
        ),
    ]
