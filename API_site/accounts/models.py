

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

# Table: ANONYMOUS_USER

class AnonymousUser(models.Model):
	Age = models.CharField("Age", max_length=3, null=True,)
	zip_code = models.CharField("ZIP", max_length=12, null=True,)
	location = models.CharField("Location", max_length=1024, null=True,) 
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
	homecity = models.CharField("Home City", max_length=1024)
	representativetown = models.CharField("Representative Town", max_length=1024)
	party = models.CharField("Party", max_length=1024)
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
		return self.name # <----to see the name in not the id 

# Table: REPRESENT
class Represent(models.Model):
	representative = models.ForeignKey(Representative, null=True, on_delete= models.SET_NULL) # one to many relationship
	anonymous = models.ForeignKey(AnonymousUser, null=True, on_delete= models.SET_NULL) # one to many relationship

	def __str__(self):
		return self.anonymous.name # <----to see the name in not the id 


# Table: EDUCATION
class Education(models.Model):
	schoolname = models.CharField("School Name", max_length=200, null=True)
	location = models.CharField("Location", max_length=1024)
	level = models.CharField("School Name", max_length=200, null=True)
	program = models.CharField("Program", max_length=200, null=True)

	def __str__(self):
		return self.name # <----to see the name in not the id 


# Table: ALL_EDUCATION
class AllEducation(models.Model):
	representative = models.ForeignKey(Representative, null=True, on_delete= models.SET_NULL) # one to many relationship
	education = models.ForeignKey(Education, null=True, on_delete= models.SET_NULL) # one to many relationship

	def __str__(self):
		return self.education.name # <----to see the name in not the id 


# Table: EXPERIENCE	
class Experience(models.Model):
	companyname = models.CharField("Company Name", max_length=200, null=True)
	location = models.CharField("Location", max_length=1024)
	type = models.CharField("Type", max_length=200, null=True)
	experienceyear = models.CharField("Year", max_length=3, null=True)

	def __str__(self):
		return self.name # <----to see the name in not the id 


# Table: ALL_EXPERIENCE		
class AllExperience(models.Model):
	representative = models.ForeignKey(Representative, null=True, on_delete= models.SET_NULL) # one to many relationship
	experience = models.ForeignKey(Experience, null=True, on_delete= models.SET_NULL) # one to many relationship

	def __str__(self):
		return self.experience.name # <----to see the name in not the id 


# Table: VOTE
class Vote(models.Model):
	BillNumber = models.CharField("Company Name", max_length=200, null=True)
	Date = models.DateField('Date', null=True, blank=True)
	Description = models.CharField("Location", max_length=1024)
	Status = models.CharField("Location", max_length=50)

	def __str__(self):
		return self.name # <----to see the name in not the id 


# Table: ALL_VOTES	
class AllVote(models.Model):
	representative = models.ForeignKey(Representative, null=True, on_delete= models.SET_NULL) # one to many relationship
	vote = models.ForeignKey(Vote, null=True, on_delete= models.SET_NULL) # one to many relationship

	def __str__(self):
		return self.vote.name # <----to see the name in not the id 


# Table: SPONSOR
class Sponsor(models.Model):
	organization = models.CharField("Organization Name", max_length=200, null=True)
	amount = models.CharField("Amount", max_length=50)
	#  amount_currency = MoneyField(decimal_places=2, default=0, default_currency='USD', max_digits=11,)

	def __str__(self):
		return self.name # <----to see the name in not the id 


# Table: ALL_SPONSOR	
class AllSponsor(models.Model):
	representative = models.ForeignKey(Representative, null=True, on_delete= models.SET_NULL) # one to many relationship
	sponsor = models.ForeignKey(Sponsor, null=True, on_delete= models.SET_NULL) # one to many relationship

	def __str__(self):
		return self.sponsor.name # <----to see the name in not the id 


# Table: DONATION
class Sector(models.Model):
	sector = models.CharField("Sector Name", max_length=200, null=True)
	amount = models.CharField("Amount", max_length=50)
	#  amount_currency = MoneyField(decimal_places=2, default=0, default_currency='USD', max_digits=11,)

	def __str__(self):
		return self.name # <----to see the name in not the id 


# Table: ALL_DONATIONS
class AllSector(models.Model):
	representative = models.ForeignKey(Representative, null=True, on_delete= models.SET_NULL) # one to many relationship
	sector = models.ForeignKey(Sector, null=True, on_delete= models.SET_NULL) # one to many relationship

	def __str__(self):
		return self.vote.name # <----to see the name in not the id 