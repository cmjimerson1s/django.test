# Generated by Django 3.2.19 on 2023-05-05 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testing_ground', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reservation',
            options={'ordering': ['-date']},
        ),
    ]
