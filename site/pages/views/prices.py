from django.shortcuts import render
from packages import models as packages_models


def prices(request):

    if request.account is not None:
        owned_packages = set(
            request.account.package_history.active().values_list(
                'package_id',
                flat=True
            )
        )
        owned_packages.add(packages_models.Package.free_package().id)
    else:
        owned_packages = set()

    return render(request, 'pages/prices.html', {
        'packages': packages_models.Package.all(),
        'owned_packages': owned_packages,
    })
