# Generated by Django 5.2.1 on 2025-06-05 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0009_category_book_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Library',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Library Title')),
                ('location', models.CharField(blank=True, max_length=100, null=True, verbose_name='Location')),
                ('website', models.URLField(blank=True, null=True, verbose_name='Website')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='libraries',
            field=models.ManyToManyField(related_name='books', to='library.library', verbose_name='Library'),
        ),
    ]
