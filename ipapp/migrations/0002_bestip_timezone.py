# Generated by Django 2.2 on 2021-03-10 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bestip',
            name='timezone',
            field=models.CharField(default='America', max_length=100),
            preserve_default=False,
        ),
    ]