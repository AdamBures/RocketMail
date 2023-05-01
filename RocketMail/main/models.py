from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, FileExtensionValidator

# Create your models here.

def get_default():
    return "This user has not set this part."


class User(models.Model):
	username = models.CharField(max_length=30)
	password = models.CharField(max_length=15, validators=[MinLengthValidator(8), MaxLengthValidator(15)])
	created_at = models.DateTimeField(auto_now_add=True)
	first_name = models.CharField(max_length=100, default=get_default)
	last_name = models.CharField(max_length=100, default=get_default)
	
	gmail_username = models.CharField(max_length=100, default=get_default)
	gmail_password = models.CharField(max_length=100, default=get_default)


class Email(models.Model):
	sender = models.CharField(max_length=30)
	recipient = models.CharField(max_length=30)
	content = models.CharField(max_length=30)
	IPFS = models.FileField(upload_to="IPFS/", validators=[FileExtensionValidator(allowed_extensions=["pdf", "rtf", "txt"])])
