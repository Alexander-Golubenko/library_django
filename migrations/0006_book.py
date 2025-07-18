# Generated by Django 5.2.1 on 2025-06-04 09:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_alter_author_date_of_birth_alter_author_first_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Book Title')),
                ('publication_date', models.DateField(null=True, verbose_name='Publication Date')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='library.author', verbose_name='Author')),
            ],
        ),
    ]
