from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model\

User = get_user_model()
# Create your views here.


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username") or None
        password = request.POST.get("password") or None
        if all([username, password]):
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print('login here')
                return redirect('/')
    return render(request, "auth/login.html")


def register_view(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username') or None
        email = request.POST.get('email') or None
        password = request.POST.get('password') or None
        # Django FORMS
        # user_exits_qs = User.objects.filter(username__iexact=username)
        # email_exits_qs = User.objects.filter(email__iexact=email)
        try:
            User.objects.create_user(
                username=username, email=email, password=password)
        except:
            pass
    return render(request, "auth/register.html")
