

from django.db import models
from django.contrib.auth.models import User
from address.models import AddressField
# from djmoney.models.fields import MoneyField
from django.core.validators import MinValueValidator, MaxValueValidator
# from .models.address import BaseBillingAddress
# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE) # <-- add this for the User profile create a one to one relationship (customer - User)
	name = models.CharField(max_length=200, null=True) 
	Age = models.CharField("Age", max_length=3, null=True,)
	#address = AddressField(related_name='+', blank=True, null=True)
	#address1 = models.CharField("Address 1", max_length=1024)
	zip_code = models.CharField("ZIP", max_length=12, null=True,)
	city = models.CharField("City", max_length=1024, null=True,) 
	agriculture_and_food = models.IntegerField("Agriculture and Food", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	armedforces_and_nationalsecurity = models.IntegerField("Armed Forces and National Security", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	crime_and_lawenforcement = models.IntegerField("Crime and Law Enforcement", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	civilrights_and_liberties_minorityissues = models.IntegerField("Civil Rights and Liberties, Minority Issues", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	economics_and_public_finance = models.IntegerField("Economics and Public Finance", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	education = models.IntegerField("Education", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	emergency_management = models.IntegerField("Emergency Management", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	environmental_protection = models.IntegerField("Environmental Protection", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	governmentoperations_and_politics = models.IntegerField("Government Operations and Politics", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	health = models.IntegerField("Health", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	immigration = models.IntegerField("Immigration", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	internationalaffairs = models.IntegerField("International Affairs", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	labor_and_employment = models.IntegerField("Labor and Employment", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	science_technology_communications = models.IntegerField("Science, Technology, Communications", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	social_welfare = models.IntegerField("Social Welfare", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	taxation = models.IntegerField("Taxation", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	transportation_and_public_works = models.IntegerField("Transportation and Public Works", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

	def __str__(self):
		return self.name # <----to see the name in not the id 

#Table: REPRESENTATIVE
class Representative(models.Model):
	firstname = models.CharField("FirstName", max_length=200, null=True) 
	lastname = models.CharField("LastName", max_length=200, null=True)
	gender = models.CharField("Gender", max_length=1, null=True,) 
	birth_date = models.DateField('Date of Birth', null=True, blank=True)
	officeaddress = models.CharField("Office Address", max_length=1024, null=True, blank=True)
	phone = models.CharField("Phone", max_length=1024, null=True, blank=True)
	type = models.CharField("Type", max_length=1024, null=True, blank=True)
	#representativetown = models.CharField("Representative Town", max_length=1024)
	party = models.CharField("Party", max_length=1024, null=True, blank=True)
	# -----------------------------------value score below
	agriculture_and_food = models.IntegerField("Agriculture and Food", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	armedforces_and_nationalsecurity = models.IntegerField("Armed Forces and National Security", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	crime_and_lawenforcement = models.IntegerField("Crime and Law Enforcement", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	civilrights_and_liberties_minorityissues = models.IntegerField("Civil Rights and Liberties, Minority Issues", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	economics_and_public_finance = models.IntegerField("Economics and Public Finance", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	education = models.IntegerField("Education", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	emergency_management = models.IntegerField("Emergency Management", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	environmental_protection = models.IntegerField("Environmental Protection", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	governmentoperations_and_politics = models.IntegerField("Government Operations and Politics", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	health = models.IntegerField("Health", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	immigration = models.IntegerField("Immigration", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	internationalaffairs = models.IntegerField("International Affairs", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	labor_and_employment = models.IntegerField("Labor and Employment", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	science_technology_communications = models.IntegerField("Science, Technology, Communications", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	social_welfare = models.IntegerField("Social Welfare", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	taxation = models.IntegerField("Taxation", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	transportation_and_public_works = models.IntegerField("Transportation and Public Works", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

	def __str__(self):
		return self.firstname + ' ' + self.lastname # <----to see the name in not the id

# Table: REPRESENT
class Represent(models.Model):
	representative = models.ForeignKey(Representative, null=True, on_delete= models.SET_NULL) # one to many relationship
	anonymous = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL) # one to many relationship
	district =models.IntegerField("District", null=True, blank=True)
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
	sRoll = models.CharField("sRoll", max_length=200, null=True, blank=True)
	hrRoll = models.CharField("hrRoll", max_length=200, null=True, blank=True)
	category1 = models.CharField("category1", max_length=200, null=True, blank=True)
	category1 = models.CharField("category1", max_length=200, null=True, blank=True)
	organizationSponsor1 = models.CharField(" Sponsor1", max_length=200, null=True, blank=True)
	organizationSponsor2 = models.CharField(" Sponsor2", max_length=200, null=True, blank=True)	
	organizationSponsor3 = models.CharField(" Sponsor3", max_length=200, null=True, blank=True)	
	organizationSponsor4 = models.CharField(" Sponsor4", max_length=200, null=True, blank=True)	

	def __str__(self):
		return self.number # <----to see the name in not the id 


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

