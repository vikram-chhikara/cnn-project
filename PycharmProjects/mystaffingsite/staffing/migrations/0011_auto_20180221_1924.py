# Generated by Django 2.0.2 on 2018-02-21 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staffing', '0010_auto_20180213_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='company_name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
