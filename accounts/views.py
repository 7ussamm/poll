from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from .forms import user_registration_form
from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username') # username and password are the name='' we modified in the login form
        password = request.POST.get('password')
        user_auth = authenticate(request, username=username, password=password)
        if user_auth is not None:
            login(request, user_auth) # This logging in the user when he fills in the fields requiered
            redirect_url = request.GET.get('next', 'home') # 'next' when can see it by doing print(requset.GET)
                                                           # 'home' will redirect the user to home page if didn't find 'next'
                                                           # 'home' is considered the default value if there's no 'next'
                                                           
            return redirect(redirect_url) # This redirect one replaces the next two ways
            # return HttpResponseRedirect(reverse('home')) # home is tne name from the main urls.py
            # return render(request, 'home.html', context=None) use this also for same requalt above
        else:
            messages.error(request, 'Invalid Username or Password !!')
    return render(request, 'accounts/login.html', context=None)

def user_logout(request):
    logout(request)
    return redirect('home')

def user_registration(request):
    form = user_registration_form(request.POST)
    # form = UserCreationForm(request.POST) # search for it when needed
    if request.method == 'POST':

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            # # cleaned_data is an object for forms which is a dictionary
            # # we can see it by doing print(form.cleaned_data)
            # # we can do the above in another way which is
            # # username = request.POST.get('username') which will get the username from the form directly
            #
            # # to create new user using User class we imported above
            user = User.objects.create_user(username, email=email, password=password)
            form.save()
            messages.success(request, 'Thanks {} For Registration !!'.format(username))

            return redirect('accounts:user_login')

        else:
            form = user_registration_form()
    return render(request, 'accounts/register.html', {'form':form})
