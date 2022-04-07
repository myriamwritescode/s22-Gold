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

        if Represent.objects.filter(anonymous__name=constituent.name).count() > 0:
            mysenators = Represent.objects.filter(anonymous__name=constituent.name)
            noelective = False

        else:
            mysenators = Representative.objects.all()
            noelective = True
    else:
        mysenators = Representative.objects.all()
        noelective = True


    print(mysenators)
    return render(request, 'accounts/value.html', {'senators': mysenators, 'noelective' : noelective})  # this is a dictionary {key: value}




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
    votedata.append({'agriculture': constituent.agriculture})
    votedata.append({'military_and_veterans': constituent.military_and_veterans})
    votedata.append({'education_and_labor': constituent.education_and_labor})
    votedata.append({'international_affairs': constituent.international_affairs})
    votedata.append({'defense_and_intelligence': constituent.defense_and_intelligence})
    votedata.append({'energy': constituent.energy})
    votedata.append({'healthcare': constituent.healthcare})
    votedata.append({'environment': constituent.environment})
    votedata.append({'infrastructure': constituent.infrastructure})
    votedata.append({'science_and_technology': constituent.science_and_technology})
    
    alldata.append(votedata)

    # add legislative
    votedata.append({'agriculture': legislative.agriculture})
    votedata.append({'military_and_veterans': legislative.military_and_veterans})
    votedata.append({'education_and_labor': legislative.education_and_labor})
    votedata.append({'international_affairs': legislative.international_affairs})
    votedata.append({'defense_and_intelligence': legislative.defense_and_intelligence})
    votedata.append({'energy': legislative.energy})
    votedata.append({'healthcare': legislative.healthcare})
    votedata.append({'environment': legislative.environment})
    votedata.append({'infrastructure': legislative.infrastructure})
    votedata.append({'science_and_technology': legislative.science_and_technology})

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

    
    user_score.append(constituent.agriculture)
    legislative_score.append(legislative.agriculture)
   
    user_score.append(constituent.military_and_veterans)
    legislative_score.append(legislative.military_and_veterans)
    
    user_score.append(constituent.education_and_labor)
    legislative_score.append(legislative.education_and_labor)
    
    user_score.append(constituent.international_affairs)
    legislative_score.append(legislative.international_affairs)
    
    user_score.append(constituent.defense_and_intelligence)
    legislative_score.append(legislative.defense_and_intelligence)
    
    user_score.append(constituent.energy)
    legislative_score.append(legislative.energy)
    
    user_score.append(constituent.healthcare)
    legislative_score.append(legislative.healthcare)
    
    user_score.append(constituent.environment)
    legislative_score.append(legislative.environment)
    
    user_score.append(constituent.infrastructure)
    legislative_score.append(legislative.infrastructure)
    
    user_score.append(constituent.science_and_technology)
    legislative_score.append(legislative.science_and_technology)
    
    service_vector = NP.subtract(user_score, legislative_score)
    
    #find magnitude of the resulting vector
    servicescore = math.sqrt(sum(pow(element, 2) for element in
                                 service_vector))

    print ("service score:", round(servicescore,2))
    
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
        if form.is_valid:
            form.agriculture = request.POST.get('agriculture')
            form.military_and_veterans = request.POST.get('military_and_veterans')
            form.education_and_labor = request.POST.get('education_and_labor')
            form.international_affairs = request.POST.get('international_affairs')
            form.defense_and_intelligence = request.POST.get('defense_and_intelligence')
            form.energy = request.POST.get('energy')
            form.healthcare = request.POST.get('healthcare')
            form.environment = request.POST.get('environment')
            form.infrastructure = request.POST.get('infrastructure')
            form.science_and_technology = request.POST.get('science_and_technology')

            sum = 0
            sum += int(request.POST.get('agriculture'))
            sum += int(request.POST.get('military_and_veterans'))
            sum += int(request.POST.get('education_and_labor'))
            sum += int(request.POST.get('international_affairs'))
            sum += int(request.POST.get('defense_and_intelligence'))
            sum += int(request.POST.get('energy'))
            sum += int(request.POST.get('healthcare'))
            sum += int(request.POST.get('environment'))
            sum += int(request.POST.get('infrastructure'))
            sum += int(request.POST.get('science_and_technology'))

            if sum == 100:
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

    votedata.append({'agriculture': constituent.agriculture})
    votedata.append({'military_and_veterans': constituent.military_and_veterans})
    votedata.append({'education_and_labor': constituent.education_and_labor})
    votedata.append({'international_affairs': constituent.international_affairs})
    votedata.append({'defense_and_intelligence': constituent.defense_and_intelligence})
    votedata.append({'energy': constituent.energy})
    votedata.append({'healthcare': constituent.healthcare})
    votedata.append({'environment': constituent.environment})
    votedata.append({'infrastructure': constituent.infrastructure})
    votedata.append({'science_and_technology': constituent.science_and_technology})



    print(votedata)

    return JsonResponse(votedata, safe=False)


# -------------------------------------------------------Graphing the result Data
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'admin'])
def resultsDataDemographics(request):
    votedata = []  # built and empty array
    votedata_demographics = []
    alldata = []
    demographics_agriculture_value = 0
    demographics_military_and_veterans_value = 0
    demographics_education_and_labor_value = 0
    demographics_international_affairs_value = 0
    demographics_defense_and_intelligence_value = 0
    demographics_energy_value = 0
    demographics_healthcare_value = 0
    demographics_environment_value = 0
    demographics_infrastructure_value = 0
    demographics_science_and_technology_value = 0

    if hasattr(request.user, 'customer'):
        constituent = request.user.customer  # grab the by the ID of the model
        total_demographics = Customer.objects.all().filter(Age=constituent.Age).count()
        myfilter = Customer.objects.all().filter(Age=constituent.Age)
    else:
        constituent = Representative.objects.get(id=1)
        total_demographics = Customer.objects.all().count()
        myfilter = Customer.objects.all()

    votedata.append({'agriculture': constituent.agriculture})
    votedata.append({'military_and_veterans': constituent.military_and_veterans})
    votedata.append({'education_and_labor': constituent.education_and_labor})
    votedata.append({'international_affairs': constituent.international_affairs})
    votedata.append({'defense_and_intelligence': constituent.defense_and_intelligence})
    votedata.append({'energy': constituent.energy})
    votedata.append({'healthcare': constituent.healthcare})
    votedata.append({'environment': constituent.environment})
    votedata.append({'infrastructure': constituent.infrastructure})
    votedata.append({'science_and_technology': constituent.science_and_technology})

    for i in myfilter:
        demographics_agriculture_value += i.agriculture
        demographics_military_and_veterans_value += i.military_and_veterans
        demographics_education_and_labor_value += i.education_and_labor
        demographics_international_affairs_value += i.international_affairs
        demographics_defense_and_intelligence_value += i.defense_and_intelligence
        demographics_energy_value += i.energy
        demographics_healthcare_value += i.healthcare
        demographics_environment_value += i.environment
        demographics_infrastructure_value += i.infrastructure
        demographics_science_and_technology_value += i.science_and_technology


    # obtain average of result of filter demographics
    demographics_agriculture_value /= total_demographics
    votedata_demographics.append({'agriculture': demographics_agriculture_value})

    demographics_military_and_veterans_value /= total_demographics
    votedata_demographics.append({'military_and_veterans': demographics_military_and_veterans_value})

    demographics_education_and_labor_value /= total_demographics
    votedata_demographics.append({'education_and_labor': demographics_education_and_labor_value})

    demographics_international_affairs_value /= total_demographics
    votedata_demographics.append({'international_affairs': demographics_international_affairs_value})

    demographics_defense_and_intelligence_value /= total_demographics
    votedata_demographics.append({'defense_and_intelligence': demographics_defense_and_intelligence_value})

    demographics_energy_value /= total_demographics
    votedata_demographics.append({'energy': demographics_energy_value})

    demographics_healthcare_value /= total_demographics
    votedata_demographics.append({'healthcare': demographics_healthcare_value})

    demographics_environment_value /= total_demographics
    votedata_demographics.append({'environment': demographics_environment_value})

    demographics_infrastructure_value /= total_demographics
    votedata_demographics.append({'infrastructure': demographics_infrastructure_value})

    demographics_science_and_technology_value /= total_demographics
    votedata_demographics.append({'science_and_technology': demographics_science_and_technology_value})


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

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'admin'])
def bio(request, pk_test):
    legislative = TestElectedOfficial.objects.get(first_name="Sherrod")

    return render(request, 'accounts/bio.html', {'representative': legislative})

# ---------------------------------------------------------------------------------

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'admin'])
def votes(request, pk_test):
    votes = TestVote.objects.get(voter_id="156992")

    return render(request, 'accounts/votes.html', {'representative': votes})

# ---------------------------------------------------------------------------------

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'admin'])
def funding(request, pk_test):
    funding = TestVote.objects.get(voter_id="156992")

    return render(request, 'accounts/funding.html', {'representative': funding})

# ---------------------------------------------------------------------------------