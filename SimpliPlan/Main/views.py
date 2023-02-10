from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .AccountMgr import *
from Finance.models import Information


def registration_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        email = request.POST.get('email')
        if AccountMgr.register(username=username, password=password, email=email):
            return redirect('login')
        else:
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = AccountMgr.login(username=username, password=password)

        if user:
            request.session['username'] = user.username
            return redirect('home')
        else:
            errors = True
            return render(request, 'accounts/login.html', {"errors": errors})
    else:
        return render(request, 'accounts/login.html')


def account_view(request):
    if request.session.has_key('username'):
        username = request.session['username']

        user = User.user.get(username=username)
        accMgr = AccountMgr(user)
        
        if Information.objects.filter(user = username).exists():
            firstTime = False
        else:
            firstTime = True

        if request.method == 'POST':
            newEmail = request.POST.get('email')
            if accMgr.changeEmail(newEmail):
                success_message = True
            return render(request, 'accounts/account.html', {"username": username, "success_message": success_message})
        else:
            return render(request, 'accounts/account.html', {"username": username, "firstTime": firstTime})
    else:
        return render(request, 'accounts/account.html', {})


def password_change_view(request):
    if request.session.has_key('username'):
        username = request.session['username']

        if Information.objects.filter(user = username).exists():
            firstTime = False
        else:
            firstTime = True

        user = User.user.get(username=username)
        accMgr = AccountMgr(user)
        if request.method == 'POST':
            newPassword = request.POST.get('new_password2')
            if accMgr.changePassword(newPassword):
                success_message = True
            return render(request, 'accounts/password_change.html', {"username": username, "success_message": success_message})
        else:
            return render(request, 'accounts/password_change.html', {"username": username, "firstTime": firstTime})
    else:
        return render(request, 'accounts/password_change.html', {})


def logout_view(request):
    try:
        del request.session['username']
        logout(request)
    except:
        pass
    return redirect('home')


def home_view(request):
    if request.session.has_key('username'):
        username = request.session['username']

        if Information.objects.filter(user = username).exists():
            return render(request, 'home.html', {"username": username})
        else:
            firstTime = True
            return render(request, 'home.html', {"username": username,"firstTime": firstTime})
    else:
        return render(request, 'home.html', {})


def verify_username_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if AccountMgr.sendResetLink(username, request):
            return redirect('password_reset')
        else:
            errors = True
            return render(request, 'accounts/verify_username.html', {"errors": errors})
    else:
        return render(request, 'accounts/verify_username.html')


def password_reset_view(request):
    return render(request, 'accounts/password_reset_done.html')


def password_reset_confirm_view(request, username):
    if request.method == 'POST':
        password = request.POST.get('new_password2')
        if AccountMgr.resetPassword(password, username):
            return redirect('password_reset_complete')
    else:
        return render(request, 'accounts/password_reset_confirm.html')


def password_reset_complete_view(request):
    return render(request, 'accounts/password_reset_complete.html')
