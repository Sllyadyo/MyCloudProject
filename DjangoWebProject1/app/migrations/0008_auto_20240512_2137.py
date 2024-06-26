# Generated by Django 2.2.27 on 2024-05-12 18:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20240512_2042'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='image',
        ),
        migrations.AddField(
            model_name='blog',
            name='image',
            field=models.FileField(default='temp.jpg', upload_to='', verbose_name='Путь к картинке'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='posted',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2024, 5, 12, 21, 37, 13, 118601), verbose_name='Опубликована'),
        ),
    ]
