# Generated by Django 2.2.1 on 2019-05-25 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogmodel',
            name='pub_date',
            field=models.DateField(auto_now=True),
        ),
    ]
