# Generated by Django 2.0.2 on 2018-02-13 21:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staffing', '0008_auto_20180213_2037'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='applicant',
            options={'permissions': (('view_applicant_dashboard', 'Can view applicant dashboard'),)},
        ),
        migrations.AlterModelOptions(
            name='client',
            options={'permissions': (('view_client_dashboard', 'Can view client dashboard'),)},
        ),
        migrations.AlterModelOptions(
            name='manager',
            options={'permissions': (('view_manager_dashboard', 'Can view manager dashboard'), ('add_recruiters', 'Can add recruiters'), ('remove_recruiter', 'Can remove recruiters'))},
        ),
        migrations.AlterModelOptions(
            name='recruiter',
            options={'permissions': (('view_recruiter_dashboard', 'Can view recruiter dashboard'),)},
        ),
    ]
