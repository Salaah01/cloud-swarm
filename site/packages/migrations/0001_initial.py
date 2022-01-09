# Generated by Django 4.0 on 2022-01-09 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('package_duration', models.IntegerField(blank=True, help_text='Period (Days) until package expires', null=True)),
                ('instances', models.PositiveIntegerField(help_text='Number of instances per benchmark.')),
                ('requests', models.PositiveIntegerField(help_text='Number of requests per instance.')),
                ('refresh_period', models.PositiveIntegerField(help_text='Number of days between benchmark limits refresh.')),
                ('quota', models.PositiveIntegerField(help_text='Number of benchmarks allowed before the refresh period.')),
            ],
        ),
    ]
