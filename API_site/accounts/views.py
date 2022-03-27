'''

this handels the responds and render for all request for this application

'''

from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm #<---django forms for authentication
from django.contrib.auth import authenticate, login, logout #<---authentication 
from django.contrib import messages #<---this for flash messages: one-time message send to the template
from django.contrib.auth.decorators import login_required #<---for every view that need to be restiction
from django.contrib.auth.models import Group
from django.urls import reverse
from django.http import JsonResponse


# Create your views here for the path response

from .models import *
from .forms import CreateUserForm,CustomerForm #we need to import to pass it to the template
#from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only #permision


#def home(request):
	#return HttpResponse('home page') #static HttpResponse
#-------------------------------------------------------------------------------User Registration
@unauthenticated_user
def registerPage(request):  
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)#<--process the form
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			messages.success(request, 'Account was created for ' + username)#<--flash messages

			return redirect('login')
		

	context = {'form':form}
	return render(request, 'accounts/register.html', context)


#-----------------------------------------------------------------------------login User 
@unauthenticated_user
def loginPage(request):

		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home') #<--- send user to the home page if they are authenticate
			else:
				messages.info(request, 'Username OR password is incorrect')#<---flash messages

		context = {}
		return render(request, 'accounts/login.html', context)
#-----------------------------------------------------------------------------logout
def logoutUser(request):
	logout(request) #<--process this logout method
	return redirect('login')
#-----------------------------------------------------------------------admin home page
@login_required(login_url='login')#<-----page restiction
@admin_only #<------only admin permission
def home(request):
	customers = Customer.objects.all()#<----querying the database
	total_customers = customers.count()
	context = { 'customers':customers}
	return render(request, 'accounts/profile.html', context)


#--------------------------------------------------------------------------User home page
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer','admin'])
def userPage(request):
	return render(request, 'accounts/profile.html')



#--------------------------------------------------------------------------User comaper home page
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer','admin'])
def comparePage(request):
	return render(request, 'accounts/compare.html')

#--------------------------------------------------------------------------User value page
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer','admin'])
def valuePage(request):
	senators = Representative.objects.all()  # create a variable for senators, think of this as a list()
	return render(request, 'accounts/value.html', {'senators': senators})  # this is a dictionary {key: value}
#--------------------------------------------------------------------------User value learn more page
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer','admin'])
def valuePagelearnmore(request):
	return render(request, 'accounts/learn_more.html')

#--------------------------------------------------------------------------update profile user only

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':  #healding the submition
		form = CustomerForm(request.POST, instance=customer)#<---no pillow (request.POST, request.FILES,instance=customer)
		if(form.is_valid):
			form.military = request.POST.get('military')
			form.government = request.POST.get('government')
			form.education = request.POST.get('education')
			form.healthcare_and_medicare = request.POST.get('healthcare_and_medicare')
			form.veteran_affairs = request.POST.get('veteran_affairs')
			form.housing_and_labor = request.POST.get('housing_and_labor')
			form.international_affairs = request.POST.get('international_affairs')
			form.energy_and_environment = request.POST.get('energy_and_environment')
			form.Science = request.POST.get('Science')
			form.transportation_and_infrastructure = request.POST.get('transportation_and_infrastructure')
			form.food_and_agriculture = request.POST.get('food_and_agriculture')
			form.socialsecurity_or_unemployment = request.POST.get('socialsecurity_or_unemployment')

			sum = 0
			sum += int(request.POST.get('military'))
			sum += int(request.POST.get('government'))
			sum += int(request.POST.get('education'))
			sum += int(request.POST.get('healthcare_and_medicare'))
			sum += int(request.POST.get('veteran_affairs'))
			sum += int(request.POST.get('housing_and_labor'))
			sum += int(request.POST.get('international_affairs'))
			sum += int(request.POST.get('energy_and_environment'))
			sum += int(request.POST.get('Science'))
			sum += int(request.POST.get('transportation_and_infrastructure'))
			sum += int(request.POST.get('food_and_agriculture'))
			sum += int(request.POST.get('socialsecurity_or_unemployment'))
			
			if(sum == 100):
				form.save()
				messages.success(request, 'Profile succesfully updated!')
			else:
				messages.error(request, 'Value scores do not total 100')

	context = {'form':form}
	return render(request, 'accounts/account_settings.html', context)

#----------------------------------------------------

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])	
def customer(request, pk_test): #<----show information of a paticular user
	customer = Customer.objects.get(id=pk_test)#<----querying the database for a paticular user----
	context = {'customer':customer}
	return render(request, 'accounts/profile.html',context) #dynamic 

#-------------------------------------------------------------------------------GRAPHS
