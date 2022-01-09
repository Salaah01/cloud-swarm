"""Migration to create the free package."""

from django.db import migrations


def create_free_package(apps, schema_editor):
    """Create the free package."""
    Package = apps.get_model('packages', 'Package')
    Package.objects.create(
        id=1,
        name='Free',
        description='Free package',
        price=0,
        package_duration=None,
        instances=3,
        requests=100,
        refresh_period=7,
        quota=3
    ).save()


class Migration(migrations.Migration):
    dependencies = [
        ('packages', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(create_free_package),
    ]
