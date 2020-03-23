# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0005_auto_20200109_1752'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='editor',
            options={'verbose_name_plural': 'Editores'},
        ),
        migrations.AlterModelOptions(
            name='libro',
            options={'verbose_name_plural': 'Libros'},
        ),
        migrations.AlterField(
            model_name='libro',
            name='portada',
            field=models.ImageField(null=True, upload_to=b'portadas', blank=True),
        ),
    ]
