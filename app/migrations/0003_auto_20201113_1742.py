# Generated by Django 3.1.2 on 2020-11-13 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_likeanswer_likequestion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likeanswer',
            name='state',
            field=models.BooleanField(default=None, null=True, verbose_name='Состояние отметки'),
        ),
        migrations.AlterField(
            model_name='likequestion',
            name='state',
            field=models.BooleanField(default=None, null=True, verbose_name='Состояние отметки'),
        ),
    ]
