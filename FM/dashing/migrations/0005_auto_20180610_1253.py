# Generated by Django 2.0.5 on 2018-06-10 02:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashing', '0004_auto_20180601_1914'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='query',
            options={'ordering': ['task', '-time_add']},
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['id']},
        ),
    ]
