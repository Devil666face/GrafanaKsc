# Generated by Django 4.1.4 on 2022-12-12 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0004_rename_updated_at_childserver_time_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='childserver',
            old_name='time',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='mainserver',
            old_name='time',
            new_name='updated_at',
        ),
    ]
