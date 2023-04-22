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

    # import imaplib
    # import email

    # # connect to the email server
    # mail = imaplib.IMAP4_SSL('imap.example.com')
    # mail.login('username', 'password')

    # # select the mailbox you want to fetch emails from
    # mail.select('inbox')

    # # search for emails that match your criteria
    # status, email_ids = mail.search(None, 'FROM', 'example@example.com')

    # # loop through the email ids and fetch the emails
    # for email_id in email_ids[0].split():
    #     status, email_data = mail.fetch(email_id, '(RFC822)')
    #     email_message = email.message_from_bytes(email_data[0][1])

    #     # process the email message as desired
    #     print('From:', email_message['From'])
    #     print('Subject:', email_message['Subject'])
    #     print('Body:', email_message.get_payload())
        
    # # close the connection to the email server
    # mail.close()
    # mail.logout()

    
    if request.session.get('LOGGED', True):
        return render(request, 'profile.html', {'username': username})
    else:
        return redirect('login')

def check_email_source(email_message):
    # get the originating IP address of the email server
    ip_address = email_message.get("Received").split(" ")[1]
    
    # get the domain name of the email server
    domain_name = email.utils.parseaddr(email_message.get("From"))[1].split("@")[1]

    # check if the email is coming from a Web3 email server
    if ip_address.startswith("127.0.0.1") and domain_name.endswith(".eth"):
        return "Web3"
    # check if the email is coming from a Web2 email server
    else:
        return "Web2"

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

# def send_email(request):
#     return redirect(f'/')

def logout_view(request):
    logout(request)
    return redirect('login')
