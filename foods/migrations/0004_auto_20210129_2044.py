# Generated by Django 3.1.5 on 2021-01-29 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0003_auto_20210129_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='photo',
            field=models.ImageField(upload_to=''),
        ),
    ]