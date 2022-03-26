

from django.db import models
from django.contrib.auth.models import User
#from address.models import AddressField
from django.utils.translation import ugettext_lazy as _
# from djmoney.models.fields import MoneyField
from django.core.validators import MinValueValidator, MaxValueValidator
# from .models.address import BaseBillingAddress
# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE) # <-- add this for the User profile create a one to one relationship (customer - User)
	name = models.CharField(max_length=200, null=True) 
	Age = models.CharField("Age", max_length=3, null=True,)
	#address = AddressField(related_name='+', blank=True, null=True)
	number = models.CharField(_('Number'), max_length = 30, null=True, blank = True)
	street_line1 = models.CharField(_('Address 1'), max_length = 100, null=True, blank = True)
	street_line2 = models.CharField(_('Address 2'), max_length = 100, null=True, blank = True)
	zipcode = models.CharField(_('ZIP code'), max_length = 5, null=True, blank = True)
	city = models.CharField(_('City'), max_length = 100, null=True, blank = True)
	state = models.CharField(_('State'), max_length = 100, null=True, blank = True)
	# -----------------------------------value score below
	military = models.IntegerField("Military", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	government = models.IntegerField("Government", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	education = models.IntegerField("Education", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	healthcare_and_medicare = models.IntegerField("Healthcare and Medicare", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	veteran_affairs = models.IntegerField("Veteran's Affairs", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	housing_and_labor = models.IntegerField("Housing and Labor", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	international_affairs = models.IntegerField("International Affairs", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	energy_and_environment = models.IntegerField("Energy and Environment", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	Science = models.IntegerField("Science", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	transportation_and_infrastructure = models.IntegerField("Transportation and Infrastructure", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	food_and_agriculture = models.IntegerField("Food and Agriculture", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	socialsecurity_or_unemployment = models.IntegerField("Social Security or Unemployment", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	def __str__(self):
		return self.name # <----to see the name in not the id 

#Table: REPRESENTATIVE
class Representative(models.Model):
	firstname = models.CharField("FirstName", max_length=200, null=True) 
	lastname = models.CharField("LastName", max_length=200, null=True)
	gender = models.CharField("Gender", max_length=1, null=True,) 
	birth_date = models.DateField('Date of Birth', null=True, blank=True)
	officeaddress = models.CharField("Office Address", max_length=1024, null=True, blank=True)
	#number = models.CharField(_('Number'), max_length = 30, null=True, blank = True)
	#street_line1 = models.CharField(_('Address 1'), max_length = 100, null=True, blank = True)
	#street_line2 = models.CharField(_('Address 2'), max_length = 100, null=True, blank = True)
	#zipcode = models.CharField(_('ZIP code'), max_length = 5, null=True, blank = True)
	#city = models.CharField(_('City'), max_length = 100, null=True, blank = True)
	state = models.CharField(_('State'), max_length = 100, null=True, blank = True)
	district =models.IntegerField("District", null=True, blank=True)
	phone = models.CharField("Phone", max_length=1024, null=True, blank=True)
	type = models.CharField("Type", max_length=1024, null=True, blank=True)
	#representativetown = models.CharField("Representative Town", max_length=1024)
	party = models.CharField("Party", max_length=1024, null=True, blank=True)
	# -----------------------------------value score below
	military = models.IntegerField("Military", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	government = models.IntegerField("Government", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	education = models.IntegerField("Education", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	healthcare_and_medicare = models.IntegerField("Healthcare and Medicare", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	veteran_affairs = models.IntegerField("Veteran's Affairs", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	housing_and_labor = models.IntegerField("Housing and Labor", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	international_affairs = models.IntegerField("International Affairs", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	energy_and_environment = models.IntegerField("Energy and Environment", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	Science = models.IntegerField("Science", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	transportation_and_infrastructure = models.IntegerField("Transportation and Infrastructure", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	food_and_agriculture = models.IntegerField("Food and Agriculture", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	socialsecurity_or_unemployment = models.IntegerField("Social Security or Unemployment", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])


	def __str__(self):
		return self.firstname + ' ' + self.lastname # <----to see the name in not the id

# Table: REPRESENT
class Represent(models.Model):
	representative = models.ForeignKey(Representative, null=True, on_delete= models.SET_NULL) # one to many relationship
	anonymous = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL) # one to many relationship
	#district =models.IntegerField("District", null=True, blank=True)
	state =models.CharField("State", max_length=1024, null=True, blank=True)
	servicescore = models.IntegerField("Service Score", null=True, blank=True)

	def __str__(self):
		return self.anonymous.name # <----to see the name in not the id 

# Table: BILL
class Bill(models.Model):
	number = models.CharField("Bill Number", max_length=200, null=True)
	date = models.DateField('Date', null=True, blank=True)
	outcome = models.CharField("Vote Result", max_length=200,null=True, blank=True)
	description = models.CharField("Description", max_length=1024, null=True, blank=True)
	#sRoll = models.CharField("Senate Vote Number", max_length=200, null=True, blank=True)
	sRoll =models.IntegerField("Senate Vote Number", null=True, blank=True)
	hrRoll =models.IntegerField("House Roll", null=True, blank=True)
	#hrRoll = models.CharField("House Roll", max_length=200, null=True, blank=True)


	def __str__(self):
		return self.number # <----to see the name in not the id 


# Table: Committee
class Committee(models.Model):
	number =models.IntegerField("Committee Number", null=True)
	category = models.CharField("Category ", max_length=200, null=True)
	hrname = models.CharField("House Committee Name", max_length=250, null=True, blank=True)
	sname = models.CharField("Senate Committee Name", max_length=250, null=True, blank=True)

	def __str__(self):
		return  self.category # <----to see the name in not the id 


# Table: Committees
class Committees(models.Model):
	committee = models.ForeignKey(Committee, null=True, on_delete= models.SET_NULL) # one to many relationship
	bill = models.ForeignKey(Bill, null=True, on_delete= models.SET_NULL) # one to many relationship

	def __str__(self):
		return self.bill.number +' '+ self.committee.category # <----to see the name in not the id 

# Table: Sponsor
class Sponsor(models.Model):
	#name = models.CharField("Name", max_length=250, null=True)
	lastname = models.CharField("LastName", max_length=200, null=True)
	firstname = models.CharField("FirstName", max_length=200, null=True)
	
	def __str__(self):
		return self.firstname + ' ' + self.lastname # <----to see the name in not the id 

# Table: Sponsors
class Sponsors(models.Model):
	sponsor = models.ForeignKey(Sponsor, null=True, on_delete= models.SET_NULL) # one to many relationship
	bill = models.ForeignKey(Bill, null=True, on_delete= models.SET_NULL) # one to many relationship

	def __str__(self):
		return self.bill.number +' '+ self.sponsor.firstname +' '+ self.sponsor.lastname# <----to see the name in not the id 

# Table: VOTES	
class Votes(models.Model):
	# BillNumber = models.CharField("BillNumber", max_length=200, null=True)
	roll =models.IntegerField("Roll", null=True, blank=True)
	date = models.DateField('Date', null=True, blank=True)
	voteCast = models.CharField("Vote Cast", max_length=3, null=True)
	representative = models.ForeignKey(Representative, null=True, on_delete= models.SET_NULL) # one to many relationship
	vote = models.ForeignKey(Bill, null=True, on_delete= models.SET_NULL) # one to many relationship

	def __str__(self):
		return self.vote.number +' '+ self.representative.firstname + ' ' + self.representative.lastname # <----to see the name in not the id 

