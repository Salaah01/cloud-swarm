from django.shortcuts import render


def prices(request):
    return render(request, 'pages/prices.html')
