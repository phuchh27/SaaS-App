from django.http import HttpResponse
import pathlib
from django.shortcuts import render

from visits.models import PageVisit
this_dir = pathlib.Path(__file__).resolve().parent


def home_page_view(request, *args, **kwargs):
    qs = PageVisit.objects.all()
    page_ps = PageVisit.objects.filter(path=request.path)
    my_title = "Home"
    html_tamplate = "home.html"
    my_context = {
        "page_title": my_title,
        "queryset_count": page_ps.count(),
        'total_visit_count': qs.count()
    }
    PageVisit.objects.create(path=request.path)
    return render(request, html_tamplate, my_context)
