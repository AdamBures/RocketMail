from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail

from .models import User, Email
from .rocketEncryption import DiffieHellman

import os

from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import ssl
import smtplib
import requests
import binascii

from dotenv import load_dotenv

load_dotenv()

# Create your views here.
def index(request):
    return render(request, "index.html")

def get_from_IPFS(cid):
    email = Email.objects.filter(cid=cid)[0]

    content = email.message


    return content

def my_view(request, **kwargs):
    username = kwargs.get('username')

    if request.session.get('LOGGED', True):

        user = User.objects.filter(username=username)[0]
        password = user.password
        first_name = user.first_name
        last_name = user.last_name
        gmail_username = user.gmail_username
        gmail_password = user.gmail_password

        message = ""
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            gmail_username = request.POST.get('gmail_username')
            gmail_password = request.POST.get('gmail_password')

            user.username = username
            user.password = password
            user.first_name = first_name
            user.last_name = last_name

            context = ssl.create_default_context()
            smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
            try:
                smtp.login(gmail_username, gmail_password)
                user.gmail_username = gmail_username
                user.gmail_password = gmail_password
            except:
                message = 'Invalid gmail username or password. If your credentials are correct please add an app to your Google account.'

            user.save()

        return render(request, 'profile.html', {'username': username, 'password': password, 'first_name': first_name, 'last_name': last_name, 'gmail_username': gmail_username, 'gmail_password': gmail_password, 'messages': message})

    else:
        return redirect('login')

def send_web2_email(subject, message_body):
    # set up the sender and recipient email addresses
    sender_email = 'sender'
    recipient_email = 'recipient'

    # set up the message body

    # set up the message headers
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    # add the message body to the message
    message.attach(MIMEText(message_body, 'plain'))

    # set up the SMTP server
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.ehlo()
    smtp_server.starttls()

    # log in to the SMTP server
    smtp_server.login(sender_email, 'password')

    # send the email
    smtp_server.sendmail(sender_email, recipient_email, message.as_string())

    # log out of the SMTP server
    smtp_server.quit()


def send_to_IPFS(email_subject, email_content):
    sender = DiffieHellman()
    receiver = DiffieHellman()


    # Encrypt message and generate decrypted message
    encrypted_message = receiver.encrypt(sender.public_key, email_subject + "\n" + email_content)
    decrypted_message = sender.decrypt(receiver.public_key, encrypted_message, receiver.IV)

    # Define IPFS parameters and upload encrypted message to IPFS
    # Replace YOUR_API_KEY and YOUR_API_SECRET with your own IPFS credentials
    api_key = os.getenv("ipfs_api_key")
    api_secret = os.getenv("ipfs_api_secret")

    ipfs_url = 'https://api.pinata.cloud/pinning/pinFileToIPFS'
    headers = {'pinata_api_key': api_key, 'pinata_secret_api_key': api_secret}
    
    data = {'file': encrypted_message}
    response = requests.post(ipfs_url, files=data, headers=headers)
    cid = response.json()['IpfsHash']
    
    email = Email.objects.create(cid=cid, message=binascii.hexlify(decrypted_message).decode(), public_key=receiver.IV)

    return cid, receiver

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
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return render(request, 'register.html', {'messages': messages.get_messages(request)})
        else:    
            user = User.objects.create(username=username, password=password, first_name=first_name, last_name=last_name)
            user.save()
            return render(request, 'login.html')
    else:
        return render(request, "register.html")

def send_email(request):
    if request.session.get('LOGGED', True):
        if request.method == "POST":
            username = request.session["username"]
            recipient = request.POST.get('recipient')

            subject = request.POST.get('subject')

            content = request.POST.get('content')

            web = request.POST.get('web')

            if web == "Web2":
                send_mail_gmail(username, recipient, subject, content)
                return render(request, 'send.html')
            else:
                ipfs = send_to_IPFS(subject, content)


            cid = ipfs[0]
            receiver = ipfs[1]

            # Define RocketMail email parameters and send email through Django's send_mail function
            rocketmail_subject = 'You have a new message on IPFS.'
            rocketmail_message = f'Find it at: {cid}. Please use my public key and the receiver code {receiver.IV} to unlock it.'
            
            send_mail_gmail(username, recipient, rocketmail_subject, rocketmail_message)
            
            return render(request, 'send.html')
            
        else:
            return render(request, "send.html")
    else:
        return redirect('login')


def send_mail_gmail(username, recipient, rocketmail_subject, rocketmail_message):
    user = User.objects.filter(username=username)[0]
    if user.gmail_username != "This user has not set this part.":
        sender = user.gmail_username
        password = user.gmail_password
    else:
        sender = "testrocketmail@gmail.com"
        password = os.getenv("password")

    em = EmailMessage()
    em["From"] = sender
    em["To"] = recipient
    em["Subject"] = rocketmail_subject
    em.set_content(rocketmail_message)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, recipient, em.as_string())


def get_emails(request):
    return render(request, "email-list.html")

def logout_view(request):
    logout(request)
    return redirect('login')
