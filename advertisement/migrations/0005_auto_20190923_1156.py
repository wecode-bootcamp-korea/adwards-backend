# Generated by Django 2.2.4 on 2019-09-23 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0004_auto_20190922_2139'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='like_count',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='view_count',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
