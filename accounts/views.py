from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }
    return render(request, 'signup.html', context)

def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())

            # /accounts/login
            # /accounts/login/?next=/articles/create
            next_url = request.GET.get('next')

            # next가 없을 때는 None or 'articles:index'
            # next가 있을 때는 'articles/create' or 'articles:index'
            return redirect(next_url or 'articles:index')
    else:
        form = CustomAuthenticationForm(request.POST)

    context = {
        'form': form,
    }
    return render(request, 'login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('articles:index')