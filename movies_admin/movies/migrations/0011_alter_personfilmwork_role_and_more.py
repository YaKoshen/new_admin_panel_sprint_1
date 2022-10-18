# Generated by Django 4.1.2 on 2022-10-18 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0010_alter_person_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personfilmwork',
            name='role',
            field=models.TextField(blank=True, choices=[('actor', 'Actor'), ('writer', 'Writer'), ('director', 'Director')], null=True, verbose_name='Role'),
        ),
        migrations.AlterUniqueTogether(
            name='personfilmwork',
            unique_together={('filmwork', 'person', 'role')},
        ),
        migrations.AddIndex(
            model_name='filmwork',
            index=models.Index(fields=['creation_date'], name='filmwork_creatio_cacc5b_idx'),
        ),
    ]