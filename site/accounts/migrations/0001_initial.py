# Generated by Django 4.0 on 2022-01-09 19:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('packages', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expiry_date', models.DateField(blank=True, null=True)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='packages.package')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='PackageHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('expiry_date', models.DateField(blank=True, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.account')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='packages.package')),
            ],
            options={
                'verbose_name': 'Package History',
                'verbose_name_plural': 'Package History',
                'ordering': ['-created_on', '-expiry_date'],
            },
        ),
    ]
