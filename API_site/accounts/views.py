'''

this handels the responds and render for all request for this application

'''

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm  # <---django forms for authentication
from django.contrib.auth import authenticate, login, logout  # <---authentication
from django.contrib import messages  # <---this for flash messages: one-time message send to the template
from django.contrib.auth.decorators import login_required  # <---for every view that need to be restiction
from django.contrib.auth.models import Group
from django.urls import reverse
from django.http import JsonResponse
#from ..scratch_1 import servicecalculator
import numpy as NP
import math
# Create your views here for the path response

from .models import *
from .forms import CreateUserForm, CustomerForm  # we need to import to pass it to the template
# from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only  # permision


# def home(request):
# return HttpResponse('home page') #static HttpResponse
#@login_required(login_url='login')
# @allowed_users(allowed_roles=['customer', 'admin'])
# def valuePage(request):
#     legislators = TestElectedOfficial.objects.all()
#     users_reps = []
#     for legislator in legislators:
#         if legislator.state == 'VA' and (legislator.type == 'sen' or legislator.district == 2):
#             # users_reps.append(f'{legislator.first_name} {legislator.last_name} {legislator.bioguide_id}')
#             users_reps.append(legislator.bioguide_id)

#     # votes = TestVote.objects.all()
#     #
#     # bills = TestBill.objects.all()
#     # bill_ids = []
#     # for bill in bills:
#     # 	bill_ids.append(bill.bill_id)

#     x = [1, 2, 3]
#     y = [4, 5, 6]
#     z = [7, 8, 9]

#     rep_values = [x, y, z]

#     data = {'users_reps': users_reps, 'rep_values': rep_values}
#     return render(request, 'accounts/value.html', data)
#
# -------------------------------------------------------------------------------User Registration
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)  # <--process the form
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account was created for ' + username)  # <--flash messages

            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


# -----------------------------------------------------------------------------login User
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # <--- send user to the home page if they are authenticate
        else:
            messages.info(request, 'Username OR password is incorrect')  # <---flash messages

    context = {}
    return render(request, 'accounts/login.html', context)


# -----------------------------------------------------------------------------logout
def logoutUser(request):
    logout(request)  # <--process this logout method
    return redirect('login')


# -----------------------------------------------------------------------admin home page
@login_required(login_url='login')  # <-----page restiction
@admin_only  # <------only admin permission
def home(request):
    customers = Customer.objects.all()  # <----querying the database
    total_customers = customers.count()
    context = {'customers': customers}
    return render(request, 'accounts/profile.html', context)


# --------------------------------------------------------------------------User home page
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'admin'])
def userPage(request):
    return render(request, 'accounts/profile.html')


# --------------------------------------------------------------------------User comaper home page
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'admin'])
def comparePage(request):
    return render(request, 'accounts/compareCommunity.html')


# --------------------------------------------------------------------------User value page
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'admin'])
def valuePage(request):
    if hasattr(request.user, 'customer'):
        constituent = request.user.customer
        mysenators = Represent.objects.filter(anonymous__name=constituent.name)
    else:  
        mysenators = Representative.objects.all()
 

    print(mysenators)
    return render(request, 'accounts/value.html', {'senators': mysenators})  # this is a dictionary {key: value}


# -------------------------------------------------------Graphing the result Data
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'admin'])
def resultsDatalegislative(request, pk_test):
    votedata = []  # built and empty array
    votedata_legislative = []
    alldata = []
    if hasattr(request.user, 'customer'):
        constituent = request.user.customer  # grab the by the ID of the model
    else:
        constituent = Representative.objects.get(id=1)
        
     # grab the by the ID of the model
    legislative = Representative.objects.get(id=pk_test)


    # grab the all the choices
    votedata.append({'military': constituent.military})
    votedata.append({'government': constituent.government})
    votedata.append({'education': constituent.education})
    votedata.append({'healthcare_and_medicare': constituent.healthcare_and_medicare})
    votedata.append({'veteran_affairs': constituent.veteran_affairs})
    votedata.append({'housing_and_labor': constituent.housing_and_labor})
    votedata.append({'international_affairs': constituent.international_affairs})
    votedata.append({'energy_and_environment': constituent.energy_and_environment})
    votedata.append({'Science': constituent.Science})
    votedata.append({'transportation_and_infrastructure': constituent.transportation_and_infrastructure})
    votedata.append({'food_and_agricultur_value': constituent.food_and_agriculture})
    votedata.append({'socialsecurity_or_unemployment': constituent.socialsecurity_or_unemployment})

    
    alldata.append(votedata)
    # add legislative
    votedata_legislative.append({'military': legislative.military})
    votedata_legislative.append({'government': legislative.government})
    votedata_legislative.append({'education': legislative.education})
    votedata_legislative.append({'healthcare_and_medicare': legislative.healthcare_and_medicare})
    votedata_legislative.append({'veteran_affairs': legislative.veteran_affairs})
    votedata_legislative.append({'housing_and_labor': legislative.housing_and_labor})
    votedata_legislative.append({'housing_and_labor': legislative.international_affairs})
    votedata_legislative.append({'international_affairs': legislative.energy_and_environment})
    votedata_legislative.append({'Science': legislative.Science})
    votedata_legislative.append({'transportation_and_infrastructure': legislative.transportation_and_infrastructure})
    votedata_legislative.append({'food_and_agricultur_value': legislative.food_and_agriculture})
    votedata_legislative.append({'socialsecurity_or_unemployment': legislative.socialsecurity_or_unemployment})
    alldata.append(votedata_legislative)

    print(alldata)

    return JsonResponse(alldata, safe=False)  # send it to the javascript
# --------------------------------------------------------------------------User value learn more page


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'admin'])
def valuePagelearnmore(request, pk_test):
    if hasattr(request.user, 'customer'):
        constituent = request.user.customer  # grab the by the ID of the model
    else:
        constituent = Representative.objects.get(id=1)
    legislative = Representative.objects.get(id=pk_test)
   
    user_score =[]
    legislative_score =[]

    
    user_score.append(constituent.military)
    legislative_score.append(legislative.military)
   
    user_score.append(constituent.government)
    legislative_score.append(legislative.government)
    
    user_score.append(constituent.education)
    legislative_score.append(legislative.education)
    
    user_score.append(constituent.healthcare_and_medicare)
    legislative_score.append(legislative.healthcare_and_medicare)
    
    user_score.append(constituent.veteran_affairs)
    legislative_score.append(legislative.veteran_affairs)
    
    user_score.append(constituent.housing_and_labor)
    legislative_score.append(legislative.housing_and_labor)
    
    user_score.append(constituent.international_affairs)
    legislative_score.append(legislative.international_affairs)
    
    user_score.append(constituent.energy_and_environment)
    legislative_score.append(legislative.energy_and_environment)
    
    user_score.append(constituent.Science)
    legislative_score.append(legislative.Science)
    
    user_score.append(constituent.transportation_and_infrastructure)
    legislative_score.append(legislative.transportation_and_infrastructure)
    
    user_score.append(constituent.food_and_agriculture)
    legislative_score.append(legislative.food_and_agriculture)
    
    user_score.append(constituent.socialsecurity_or_unemployment)
    legislative_score.append(legislative.socialsecurity_or_unemployment)
    
    service_vector = NP.subtract(user_score, legislative_score)
    
    #find magnitude of the resulting vector
    servicescore = math.sqrt(sum(pow(element, 2) for element in
                                 service_vector))

    print ("service score:", round (servicescore,2)) 
    
    return render(request, 'accounts/learn_more.html', {'legislative': legislative,'service':round(abs(servicescore-100),2),'incompatible':round(servicescore,2)})


# --------------------------------------------------------------------------update profile user only

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':  # healding the submition
        form = CustomerForm(request.POST,
                            instance=customer)  # <---no pillow (request.POST, request.FILES,instance=customer)
        if (form.is_valid):
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

            if (sum == 100):
                form.save()
                # messages.success(request, 'Profile succesfully updated!')
                return redirect('home')  # <--- send user to the home page if they are authenticate
            else:
                messages.error(request, 'Value scores do not total 100')

    context = {'form': form}
    return render(request, 'accounts/account_settings.html', context)


# -------------------------------------------------------Graphing the result Data
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'admin'])
def resultsData(request):
    votedata = []  # built and empty array
    if hasattr(request.user, 'customer'):
        constituent = request.user.customer  # grab the by the ID of the model
    else:
        constituent = Representative.objects.get(id=1)

    votedata.append({'military': constituent.military})
    votedata.append({'government': constituent.government})
    votedata.append({'education': constituent.education})
    votedata.append({'healthcare_and_medicare': constituent.healthcare_and_medicare})
    votedata.append({'veteran_affairs': constituent.veteran_affairs})
    votedata.append({'housing_and_labor': constituent.housing_and_labor})
    votedata.append({'international_affairs': constituent.international_affairs})
    votedata.append({'energy_and_environment': constituent.energy_and_environment})
    votedata.append({'Science': constituent.Science})
    votedata.append({'transportation_and_infrastructure': constituent.transportation_and_infrastructure})
    votedata.append({'food_and_agricultur_value': constituent.food_and_agriculture})
    votedata.append({'socialsecurity_or_unemployment': constituent.socialsecurity_or_unemployment})

    print(votedata)

    return JsonResponse(votedata, safe=False)


# -------------------------------------------------------Graphing the result Data
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'admin'])
def resultsDataDemographics(request):
    votedata = []  # built and empty array
    votedata_demographics = []
    alldata = []
    demographics_military_value = 0
    demographics_government_value = 0
    demographics_education_value = 0
    demographics_healthcare_and_medicare_value = 0
    demographics_veteran_affairs_value = 0
    demographics_housing_and_labor_value = 0
    demographics_international_affairs_value = 0
    demographics_energy_and_environment_value = 0
    demographics_Science_value = 0
    demographics_transportation_and_infrastructure_value = 0
    demographics_food_and_agricultur_value = 0
    demographics_socialsecurity_or_unemployment_value = 0
    if hasattr(request.user, 'customer'):
        constituent = request.user.customer  # grab the by the ID of the model
        total_demographics = Customer.objects.all().filter(Age=constituent.Age).count()
        myfilter = Customer.objects.all().filter(Age=constituent.Age)
    else:
        constituent = Representative.objects.get(id=1)
        total_demographics = Customer.objects.all().count()
        myfilter = Customer.objects.all()

    votedata.append({'military': constituent.military})
    votedata.append({'government': constituent.government})
    votedata.append({'education': constituent.education})
    votedata.append({'healthcare_and_medicare': constituent.healthcare_and_medicare})
    votedata.append({'veteran_affairs': constituent.veteran_affairs})
    votedata.append({'housing_and_labor': constituent.housing_and_labor})
    votedata.append({'international_affairs': constituent.international_affairs})
    votedata.append({'energy_and_environment': constituent.energy_and_environment})
    votedata.append({'Science': constituent.Science})
    votedata.append({'transportation_and_infrastructure': constituent.transportation_and_infrastructure})
    votedata.append({'food_and_agricultur_value': constituent.food_and_agriculture})
    votedata.append({'socialsecurity_or_unemployment': constituent.socialsecurity_or_unemployment})

    for i in myfilter:
        demographics_military_value += i.military
        demographics_government_value += i.government
        demographics_education_value += i.education
        demographics_healthcare_and_medicare_value += i.healthcare_and_medicare
        demographics_veteran_affairs_value += i.veteran_affairs
        demographics_housing_and_labor_value += i.housing_and_labor
        demographics_international_affairs_value += i.international_affairs
        demographics_energy_and_environment_value += i.energy_and_environment
        demographics_Science_value += i.Science
        demographics_transportation_and_infrastructure_value += i.transportation_and_infrastructure
        demographics_food_and_agricultur_value += i.food_and_agriculture
        demographics_socialsecurity_or_unemployment_value += i.socialsecurity_or_unemployment

    # obtain average of result of filter demographics
    demographics_military_value /= total_demographics
    votedata_demographics.append({'military': demographics_military_value})

    demographics_government_value /= total_demographics
    votedata_demographics.append({'government': demographics_government_value})

    demographics_education_value /= total_demographics
    votedata_demographics.append({'education': demographics_education_value})

    demographics_healthcare_and_medicare_value /= total_demographics
    votedata_demographics.append({'healthcare_and_medicare': demographics_healthcare_and_medicare_value})

    demographics_veteran_affairs_value /= total_demographics
    votedata_demographics.append({'veteran_affairs': demographics_veteran_affairs_value})

    demographics_housing_and_labor_value /= total_demographics
    votedata_demographics.append({'housing_and_labor': demographics_housing_and_labor_value})

    demographics_international_affairs_value /= total_demographics
    votedata_demographics.append({'international_affairs': demographics_international_affairs_value})

    demographics_energy_and_environment_value /= total_demographics
    votedata_demographics.append({'energy_and_environment': demographics_energy_and_environment_value})

    demographics_Science_value /= total_demographics
    votedata_demographics.append({'Science': demographics_Science_value})

    demographics_transportation_and_infrastructure_value /= total_demographics
    votedata_demographics.append(
        {'transportation_and_infrastructure': demographics_transportation_and_infrastructure_value})

    demographics_food_and_agricultur_value /= total_demographics
    votedata_demographics.append({'food_and_agricultur_value': demographics_food_and_agricultur_value})

    demographics_socialsecurity_or_unemployment_value /= total_demographics
    votedata_demographics.append({'socialsecurity_or_unemployment': demographics_socialsecurity_or_unemployment_value})

    # the construct the list that need to be graph
    alldata.append(votedata)
    alldata.append(votedata_demographics)

    print(alldata)

    return JsonResponse(alldata, safe=False)  # send it to the javascript


# ----------------------------------------------------


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):  # <----show information of a paticular user
    customer = Customer.objects.get(id=pk_test)  # <----querying the database for a paticular user----
    context = {'customer': customer}
    return render(request, 'accounts/profile.html', context)  # dynamic

# -------------------------------------------------------------------------------GRAPHS
