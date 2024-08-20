"""
URL configuration for pfdhome project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from .view import (home_view, about_view, pw_protected_view,
                   user_omly_view, staff_omly_view)
from auth import views as auth_view
urlpatterns = [
    path('hello-world/',  home_view, name='home'),
    path('', home_view),
    path('login/', auth_view.login_view),
    path('register/', auth_view.register_view),
    path('protected/', pw_protected_view),
    path('protected/user-only/', user_omly_view),
    path('protected/staff-only/', staff_omly_view),
    path('admin/', admin.site.urls),
    path('about/', about_view),
    path('accounts/', include('allauth.urls')),
    path('profiles/', include('profiles.urls')),
]
