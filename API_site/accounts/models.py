

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE) # <-- add this for the User profile create a one to one relationship (customer - User)
	name = models.CharField(max_length=200, null=True)  
	#profile_pic = models.ImageField(default="profile1.png", null=True, blank=True) #pillow is not istalling 
	date_created = models.DateTimeField(auto_now_add=True, null=True)


	def __str__(self):
		return self.name # <----to see the name in not the id 
