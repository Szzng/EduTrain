# Generated by Django 3.2.8 on 2021-12-02 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_auto_20211202_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='contents',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='course',
            name='summary',
            field=models.TextField(),
        ),
    ]
