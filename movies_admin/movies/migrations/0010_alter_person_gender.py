# Generated by Django 4.1.2 on 2022-10-16 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0009_alter_filmwork_file_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='gender',
            field=models.TextField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], max_length=7, null=True, verbose_name='Gender'),
        ),
    ]