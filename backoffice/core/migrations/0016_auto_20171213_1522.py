# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-13 18:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20171124_1121'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='start_date',
            new_name='created',
        ),
        migrations.AddField(
            model_name='project',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='analysis', to='core.Project'),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='dataset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='core.Dataset'),
        ),
    ]
