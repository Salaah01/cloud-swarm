# Generated by Django 4.0 on 2021-12-31 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('benchmark', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='benchmark',
            name='completed_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]