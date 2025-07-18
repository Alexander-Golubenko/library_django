# Generated by Django 5.2.1 on 2025-06-05 09:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0014_rename_posts_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Borrow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrow_date', models.DateField(auto_now=True, verbose_name='Borrow Date')),
                ('return_date', models.DateField(verbose_name='Return Date')),
                ('is_returned', models.BooleanField(default=False, verbose_name='Is Returned')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrows', to='library.book', verbose_name='Book')),
                ('library', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrows', to='library.library', verbose_name='Library')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrows', to='library.member', verbose_name='Member')),
            ],
        ),
    ]
