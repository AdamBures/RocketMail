from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator

# Create your models here.
class User(models.Model):
	username = models.CharField(max_length=30)
	password = models.CharField(max_length=15, validators=[MinLengthValidator(8), MaxLengthValidator(15)])
	created_at = models.DateTimeField(auto_now_add=True)