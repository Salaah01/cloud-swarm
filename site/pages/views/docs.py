from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse


def breadcrumbs():
    return [
        {
            'index': 10,
            'url': reverse('pages:docs:index'),
            'label': 'Documentation',
        },
    ]


def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'pages/docs/index.html', {
        'breadcrumbs': breadcrumbs(),
        'breadcrumbs_index': 10,
    })
