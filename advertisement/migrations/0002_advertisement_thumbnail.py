# Generated by Django 2.2.4 on 2019-09-21 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='thumbnail',
            field=models.URLField(default='http://image.com', max_length=2500),
            preserve_default=False,
        ),
    ]