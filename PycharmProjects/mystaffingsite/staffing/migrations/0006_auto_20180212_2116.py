# Generated by Django 2.0.2 on 2018-02-12 21:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staffing', '0005_auto_20180212_2109'),
    ]

    operations = [
        migrations.RenameModel('JobPostingTag', 'JobPostingSkill'),
        migrations.RenameModel('ApplicantTag', 'ApplicantSkill')
    ]