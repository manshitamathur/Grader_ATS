# Generated by Django 3.0.6 on 2021-08-11 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_auto_20210811_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyval',
            name='value',
            field=models.TextField(null=True),
        ),
    ]