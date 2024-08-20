from django.http import HttpResponse
import pathlib
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from visits.models import PageVisit

this_dir = pathlib.Path(__file__).resolve().parent

LOGIN_URL = settings.LOGIN_URL


def home_view(request, *args, **kwargs):
    # print(request.user.is_authenticated, request.user.first_name)
    return about_view(request, *args, **kwargs)


def about_view(request, *args, **kwargs):
    qs = PageVisit.objects.all()
    page_ps = PageVisit.objects.filter(path=request.path)
    try:
        percent = (page_ps.count() * 100) / qs.count()
    except:
        percent = 0
    my_title = "Home"
    html_tamplate = "home.html"
    my_context = {
        "page_title": my_title,
        "queryset_count": page_ps.count(),
        'percent': percent,
        'total_visit_count': qs.count()
    }
    PageVisit.objects.create(path=request.path)
    return render(request, html_tamplate, my_context)


VALID_CODE = "abc123"


def pw_protected_view(request, *args, **kwargs):
    is_allowed = request.session.get('protected_page_allowed') or 0

    # print(request.session.get('protected_page_allowed'),
    #       type(request.session.get('protected_page_allowed')))

    if request.method == "POST":
        user_pw_sent = request.POST.get('code') or None
        if user_pw_sent == VALID_CODE:
            request.session['protected_page_allowed'] = 1
    if is_allowed:
        return render(request, "protected/view.html", {})
    return render(request, "protected/entry.html", {})


@login_required
def user_omly_view(request, *args, **kwargs):
    print(request.user.is_staff)
    return render(request, "protected/user-only.html", {})


@staff_member_required(login_url=LOGIN_URL)
def staff_omly_view(request, *args, **kwargs):
    print(request.user.is_staff)
    return render(request, "protected/user-only.html", {})
