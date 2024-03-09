from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from users.forms import CreateMemberForm
from django.contrib.auth import login, logout


def register(request):
    if request.method == 'POST':
        form = CreateMemberForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('chats')
    else:
        form = CreateMemberForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('chats')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('chats')
