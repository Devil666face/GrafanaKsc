# Generated by Django 4.1.4 on 2022-12-12 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0005_rename_time_childserver_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='childserver',
            name='updated_at',
            field=models.CharField(default='12-12-2022 10:39:53Z00:00', max_length=255),
        ),
    ]
