# Generated by Django 3.0.3 on 2020-02-26 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myweb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='myNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('date', models.CharField(max_length=15)),
                ('desc', models.TextField()),
            ],
        ),
    ]
