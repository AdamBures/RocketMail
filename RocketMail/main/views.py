from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def index(request):
	return render(request, "index.html")

def my_view(request, **kwargs):
    username = kwargs.get('username')    
    if request.session.get('LOGGED', True):
        return render(request, 'profile.html', {'username': username})
    else:
        return redirect('login')

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
            found_user = User.objects.get(id=user.id)

            if (found_user.password == password):
                request.session['LOGGED'] = True
                request.session['username'] = username
                return redirect(f'profile/{username}')
            else:
                request.session['LOGGED'] = False
                messages.error(request, 'Invalid password.')
                return redirect('login')
        
        except User.DoesNotExist:
            request.session['LOGGED'] = False
            messages.error(request, 'Invalid username.')

            return redirect('login')
    else:
        username = request.session.get('username')
        if username == None:
            request.session['LOGGED'] = False
            return render(request, 'login.html')
        else:
            return redirect(f'profile/{username}')

def register(request):
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = User.objects.create(username=username, password=password)
		user.save()

		return redirect('login')
	else:
		return render(request, "register.html")

def send_email(request):
    if request.method == "POST":
        recipient = request.POST.get('recipient')
        content = request.POST.get('content')
        ipfs = request.POST.get('ipfs')

        
    else:
        return render(request, "send.html")

def logout_view(request):
    logout(request)
    return redirect('login')
