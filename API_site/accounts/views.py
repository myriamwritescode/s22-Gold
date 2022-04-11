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
# from ..scratch_1 import servicecalculator
import numpy as NP
import math
# Create your views here for the path response

from .models import *
from .forms import CreateUserForm, CustomerForm  # we need to import to pass it to the template
# from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only  # permision


# def home(request):
# return HttpResponse('home page') #static HttpResponse
# @login_required(login_url='login')
# @allowed_users(allowed_roles=['customer', 'admin'])
# def valuePage(request):


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
    # if hasattr(request.user, 'customer'):
    #     constituent = request.user.customer
    #
    #     if Represent.objects.filter(anonymous__name=constituent.name).count() > 0:
    #         mysenators = Represent.objects.filter(anonymous__name=constituent.name)
    #         noelective = False
    #
    #     else:
    #         mysenators = Representative.objects.all()
    #         noelective = True
    # else:
    #     mysenators = Representative.objects.all()
    #     noelective = True
    #
    # print(mysenators)
    # return render(request, 'accounts/value.html', {'senators': mysenators, 'noelective' : noelective})  # this is a dictionary {key: value}

    # Create a list of the user's legislator's ids
    legislator_model = TestElectedOfficial.objects.filter(state__exact='VA')
    data = create_dict_multi_legislators(legislator_model)

    return render(request, 'accounts/value.html', data)


# -------------------------------------------------------Graphing the result Data
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'admin'])
def resultsDatalegislative(request, pk_test):
    votedata = []  # built and empty array
    votedata_legislative = []
    alldata = []
    if hasattr(request.user, 'customer'):
        constituent = request.user.customer  # grab the by the ID of the model
        print("constituent")
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
    else:
        # constituent = TestElectedOfficial.objects.get(bioguide_id='W000805')
        legislator_model = TestElectedOfficial.objects.filter(bioguide_id='W000805')
        votedata = create_list_single_legislator(legislator_model)
        alldata.append(votedata)
        print("legislative")

        # Create a list of the user's legislator's ids

        # data = create_dict_multi_legislators(legislator_model)

        # alldata.append(data)

    # grab the by the ID of the model
    legislative_model = TestElectedOfficial.objects.filter(bioguide_id=pk_test)
    # legislator_model = TestElectedOfficial.objects.filter(bioguide_id='W000805')
    votedata_legislative = create_list_single_legislator(legislative_model)

    alldata.append(votedata_legislative)
    # grab the all the choices

    print(alldata)

    return JsonResponse(alldata, safe=False)  # send it to the javascript


# --------------------------------------------------------------------------User value learn more page


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'admin'])
def valuePagelearnmore(request, pk_test):
    user_score = []
    legislative_score = []

    if hasattr(request.user, 'customer'):
        constituent = request.user.customer  # grab the by the ID of the model
        user_score.append(constituent.military)
        user_score.append(constituent.government)
        user_score.append(constituent.education)
        user_score.append(constituent.healthcare_and_medicare)
        user_score.append(constituent.veteran_affairs)
        user_score.append(constituent.housing_and_labor)
        user_score.append(constituent.international_affairs)
        user_score.append(constituent.energy_and_environment)
        user_score.append(constituent.Science)
        user_score.append(constituent.transportation_and_infrastructure)
        user_score.append(constituent.food_and_agriculture)
        user_score.append(constituent.socialsecurity_or_unemployment)
    else:
        constituent = TestElectedOfficial.objects.get(bioguide_id='W000805')
        # Create a list of the user's legislator's ids
        legislator_model = TestElectedOfficial.objects.filter(bioguide_id='W000805')
        votedata_legislative = create_list_single_legislator(legislator_model)
        user_score.append(votedata_legislative[0]['military'])
        user_score.append(votedata_legislative[1]['government'])
        user_score.append(votedata_legislative[2]['education'])
        user_score.append(votedata_legislative[3]['healthcare_and_medicare'])
        user_score.append(votedata_legislative[4]['veteran_affairs'])
        user_score.append(votedata_legislative[5]['housing_and_labor'])
        user_score.append(votedata_legislative[6]['international_affairs'])
        user_score.append(votedata_legislative[7]['energy_and_environment'])
        user_score.append(votedata_legislative[8]['Science'])
        user_score.append(votedata_legislative[9]['transportation_and_infrastructure'])
        user_score.append(votedata_legislative[10]['food_and_agricultur_value'])
        user_score.append(votedata_legislative[11]['socialsecurity_or_unemployment'])

    # grab the by the ID of the model
    # legislative = TestElectedOfficial.objects.get(bioguide_id=pk_test)
    legislator_model = TestElectedOfficial.objects.filter(bioguide_id=pk_test)
    legislator_vote_date = create_list_single_legislator(legislator_model)
    legislative_score.append(legislator_vote_date[0]['military'])
    legislative_score.append(legislator_vote_date[1]['government'])
    legislative_score.append(legislator_vote_date[2]['education'])
    legislative_score.append(legislator_vote_date[3]['healthcare_and_medicare'])
    legislative_score.append(legislator_vote_date[4]['veteran_affairs'])
    legislative_score.append(legislator_vote_date[5]['housing_and_labor'])
    legislative_score.append(legislator_vote_date[6]['international_affairs'])
    legislative_score.append(legislator_vote_date[7]['energy_and_environment'])
    legislative_score.append(legislator_vote_date[8]['Science'])
    legislative_score.append(legislator_vote_date[9]['transportation_and_infrastructure'])
    legislative_score.append(legislator_vote_date[10]['food_and_agricultur_value'])
    legislative_score.append(legislator_vote_date[11]['socialsecurity_or_unemployment'])


    #     constituent = Representative.objects.get(id=1)
    legislative = TestElectedOfficial.objects.get(bioguide_id=pk_test)
    service_vector = NP.subtract(user_score, legislative_score)

    # find magnitude of the resulting vector
    servicescore = math.sqrt(sum(pow(element, 2) for element in
                                 service_vector))
    #
    # print("service score:", round(servicescore, 2))

    return render(request, 'accounts/learn_more.html',
                  {'legislative': legislative, 'service': round(abs(servicescore - 100), 2),
                   'incompatible': round(servicescore, 2)})


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
    if hasattr(request.user, 'customer'):  # GABY WE CHANGED THIS FROM 'customer'
        print('ON TOP')
        constituent = request.user.customer  # grab the by the ID of the model
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
    else:
        # constituent = TestElectedOfficial.objects.get(bioguide_id='W000805')
        # full_list = []
        # Create a list of the user's legislator's ids
        legislator_model = TestElectedOfficial.objects.filter(bioguide_id='W000805')
        votedata = create_list_single_legislator(legislator_model)
        #votedata.append(legislator_vote_data)
        print("legislator")
        print(votedata)

    return JsonResponse(votedata, safe=False)

# -------------------------------------------------------Graphing the result Data
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'admin'])
def resultsDatalegislativeMulti(request):
    votedata = []  # built and empty array
    alldata = []
    if hasattr(request.user, 'customer'):
        constituent = request.user.customer  # grab the by the ID of the model
        print("constituent")
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
    else:
        # constituent = TestElectedOfficial.objects.get(bioguide_id='W000805')
        legislator_model = TestElectedOfficial.objects.filter(bioguide_id='W000805')
        votedata = create_list_single_legislator(legislator_model)
        alldata.append(votedata)
        print("legislative")
    # add legislative
    # get all 3 bioguide_ids 
    # for each bioguide_id return list of value scores using create_single...
    #num = 
    legislators_model = TestElectedOfficial.objects.filter(state__exact='VA')
    data = create_dict_multi_legislators(legislators_model)
    all_id =[]
    for i in range(3):
        try:
            all_id.append(data['full_list'][i]['bioguide_id'])
        except IndexError:
            break
    
    print ("\n-----------allID------------")
    print(all_id)

    for i in all_id:
        legislator_model = TestElectedOfficial.objects.filter(bioguide_id=i)
        votedata_legislative= create_list_single_legislator(legislator_model)
        alldata.append(votedata_legislative)
        
    print(alldata)

    return JsonResponse(alldata, safe=False) 
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
    # if hasattr(request.user, 'customer'):
    #     constituent = request.user.customer  # grab the by the ID of the model
    #     total_demographics = Customer.objects.all().filter(Age=constituent.Age).count()
    #     myfilter = Customer.objects.all().filter(Age=constituent.Age)
    # else:
    #     constituent = Representative.objects.get(id=1)
    #     total_demographics = Customer.objects.all().count()
    #     myfilter = Customer.objects.all()
    if hasattr(request.user, 'customer'):
        constituent = request.user.customer  # grab the by the ID of the model
        print("constituent")
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
        total_demographics = Customer.objects.all().filter(Age=constituent.Age).count()
        myfilter = Customer.objects.all().filter(Age=constituent.Age)
        # alldata.append(votedata)
    else:
        # constituent = TestElectedOfficial.objects.get(bioguide_id='W000805')
        legislator_model = TestElectedOfficial.objects.filter(bioguide_id='W000805')
        votedata = create_list_single_legislator(legislator_model)
        # alldata.append(votedata)
        myfilter = Customer.objects.all()
        total_demographics = Customer.objects.all().count()
        print("legislative")
    # votedata.append({'military': constituent.military})
    # votedata.append({'government': constituent.government})
    # votedata.append({'education': constituent.education})
    # votedata.append({'healthcare_and_medicare': constituent.healthcare_and_medicare})
    # votedata.append({'veteran_affairs': constituent.veteran_affairs})
    # votedata.append({'housing_and_labor': constituent.housing_and_labor})
    # votedata.append({'international_affairs': constituent.international_affairs})
    # votedata.append({'energy_and_environment': constituent.energy_and_environment})
    # votedata.append({'Science': constituent.Science})
    # votedata.append({'transportation_and_infrastructure': constituent.transportation_and_infrastructure})
    # votedata.append({'food_and_agricultur_value': constituent.food_and_agriculture})
    # votedata.append({'socialsecurity_or_unemployment': constituent.socialsecurity_or_unemployment})

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


def create_dict_multi_legislators(model_id):
    full_list = []
    legislator_ids = []
    for legislator in model_id:
        # This next line will need to be edited when we implement Google API
        if legislator.type == 'sen':
            legislator_ids.append(legislator.lis_id)
            full_list.append({'id': legislator.lis_id,
                              'bioguide_id': legislator.bioguide_id,
                              'f_name': legislator.first_name,
                              'l_name': legislator.last_name,
                              'full_name': legislator.full_name,
                              'agg': 0, 'mil': 0, 'ed': 0, 'intl': 0, 'def': 0,
                              'energy': 0, 'health': 0, 'env': 0, 'infra': 0,
                              'sci': 0})
        # This next line will need to be edited when we implement Google AP
        elif legislator.district == 2:
            legislator_ids.append(legislator.bioguide_id)
            full_list.append({'id': legislator.bioguide_id,
                              'bioguide_id': legislator.bioguide_id,
                              'f_name': legislator.first_name,
                              'l_name': legislator.last_name,
                              'full_name': legislator.full_name,
                              'agg': 0, 'mil': 0, 'ed': 0, 'intl': 0, 'def': 0,
                              'energy': 0, 'health': 0, 'env': 0, 'infra': 0,
                              'sci': 0})

    # Get all votes where a user's legislator voted 'Yea'
    vote_model = TestVote.objects.all()
    votes = []
    bill_numbers = []
    for vote in vote_model:
        if vote.voter_id in legislator_ids and vote.value == 'Yea':
            bill_numbers.append(vote.number)
            votes.append(vote)

    # Get all bills/committees where a user's legislator voted 'Yea'
    bill_model = TestBill.objects.all()
    bills = []
    for bill in bill_model:
        if bill.number in bill_numbers:
            bills.append(bill)

    # Link categories go committee names
    agg_terms = ['Agriculture']
    mil_terms = ['Armed Services', 'Veterans\' Affairs']
    ed_terms = ['Education and Labor', 'Small Business',
                'Health, Education, Labor, and Pensions']
    intl_terms = ['Foreign Affairs', 'Foreign Relations']
    def_terms = ['Homeland Security', 'Intelligence', 'Judiciary',
                 'Narcotics Control']
    energy_terms = ['Energy and Commerce']
    health_terms = ['Education and Labor', 'Energy and Commerce', 'Aging',
                    'Finance']
    env_terms = ['Energy and Commerce', 'Natural Resources',
                 'Energy and Natural Resources',
                 'Environment and Public Works']
    infra_terms = ['Energy and Commerce', 'Transportation and Infrastructure',
                   'Banking, Housing, and Urban Affairs',
                   'Commerce, Science and Transportation']
    sci_terms = ['Science, Space, and Technology',
                 'Commerce, Science and Transportation']

    # Add points for each category based on votes and sponsorship
    for person in full_list:  # Iterate over each user's legislator
        id_num = person.get('id')
        for vote in votes:  # Iterate over shortened votes list
            vote_id = vote.voter_id
            if id_num == vote_id and vote.value == 'Yea':  # Check for an ID match and 'Yea' vote
                vote_num = vote.number
                for bill in bills:  # Iterate over shortened bills list
                    if vote_num == bill.number:  # Check that the 'Yea' vote matches the bill
                        committee = bill.committee
                        sponsor_bonus = 0  # Initialize sponsor bonus to 0
                        # Rearrange sponsor name to match order in full_list
                        last_first = bill.sponsor
                        sponsor_split = last_first.split(', ')
                        sponsor = f'{sponsor_split[1]} {sponsor_split[0]}'
                        # Change sponsor bonus if this legeslator is the sponsor
                        if sponsor == person.get('full_name'):
                            sponsor_bonus = 10
                        # Add value points to legislators category if bill aligns with that category
                        if committee in agg_terms:
                            score = person.get('agg')
                            person['agg'] = score + 1 + sponsor_bonus
                        if committee in mil_terms:
                            score = person.get('mil')
                            person['mil'] = score + 1 + sponsor_bonus
                        if committee in ed_terms:
                            score = person.get('ed')
                            person['ed'] = score + 1 + sponsor_bonus
                        if committee in intl_terms:
                            score = person.get('intl')
                            person['intl'] = score + 1 + sponsor_bonus
                        if committee in def_terms:
                            score = person.get('def')
                            person['def'] = score + 1 + sponsor_bonus
                        if committee in energy_terms:
                            score = person.get('energy')
                            person['energy'] = score + 1 + sponsor_bonus
                        if committee in health_terms:
                            score = person.get('health')
                            person['health'] = score + 1 + sponsor_bonus
                        if committee in env_terms:
                            score = person.get('env')
                            person['env'] = score + 1 + sponsor_bonus
                        if committee in infra_terms:
                            score = person.get('infra')
                            person['infra'] = score + 1 + sponsor_bonus
                        if committee in sci_terms:
                            score = person.get('sci')
                            person['sci'] = score + 1 + sponsor_bonus

    # Add points based on committee roll
    membership_model = Membership.objects.all()
    for person in full_list:  # Iterate over each user's legislator
        bioguide = person.get('bioguide_id')
        for membership in membership_model:
            if bioguide == membership.bioguide_id:  # Check for an ID match
                committee_id = membership.thomas_id
                rank = membership.rank
                # Add value points to legislators category based on their rank in the aligning committee
                if committee_id == 'HSVC' or committee_id == 'SPAG':
                    score = person.get('health')
                    person['health'] = score + (40 - rank)
                elif committee_id == 'SSVA' or committee_id == 'SSAS' \
                        or committee_id == 'HSVR' or committee_id == 'HSAS':
                    score = person.get('mil')
                    person['mil'] = score + (40 - rank)
                elif committee_id == 'SSSB' or committee_id == 'SSHR' \
                        or committee_id == 'HSSM' or committee_id == 'HSED':
                    score = person.get('ed')
                    person['ed'] = score + (40 - rank)
                elif committee_id == 'SSJU' or committee_id == 'SSGA' \
                        or committee_id == 'SLIN' or committee_id == 'SCNC' \
                        or committee_id == 'HSJU' or committee_id == 'HLIG' \
                        or committee_id == 'HSHM':
                    score = person.get('def')
                    person['def'] = score + (40 - rank)
                elif committee_id == 'SSFR' or committee_id == 'JCSE' \
                        or committee_id == 'HSFA':
                    score = person.get('intl')
                    person['intl'] = score + (40 - rank)
                elif committee_id == 'SSFI' or committee_id == 'SSCM' \
                        or committee_id == 'SSBK' or committee_id == 'JSEC' \
                        or committee_id == 'HSPW':
                    score = person.get('infra')
                    person['infra'] = score + (40 - rank)
                elif committee_id == 'SSEV' or committee_id == 'HSCN' \
                        or committee_id == 'HSII':
                    score = person.get('env')
                    person['env'] = score + (40 - rank)
                elif committee_id == 'SSEG' or committee_id == 'HSIF':
                    score = person.get('energy')
                    person['energy'] = score + (40 - rank)
                elif committee_id == 'SSCM' or committee_id == 'HSSY':
                    score = person.get('sci')
                    person['sci'] = score + (40 - rank)
                elif committee_id == 'SSAF' or committee_id == 'HSAG':
                    score = person.get('agg')
                    person['agg'] = score + (40 - rank)

    # Adjust category scores based on 100 point maximum
    for person in full_list:
        agg = person.get('agg')
        mil = person.get('mil')
        ed = person.get('ed')
        intl = person.get('intl')
        defen = person.get('def')
        energy = person.get('energy')
        health = person.get('health')
        env = person.get('env')
        infra = person.get('infra')
        sci = person.get('sci')

        total = agg + mil + ed + intl + defen + energy + health + env + infra + sci

        person['agg'] = round(agg / total * 100)
        person['mil'] = round(mil / total * 100)
        person['ed'] = round(ed / total * 100)
        person['intl'] = round(intl / total * 100)
        person['def'] = round(defen / total * 100)
        person['energy'] = round(energy / total * 100)
        person['health'] = round(health / total * 100)
        person['env'] = round(env / total * 100)
        person['infra'] = round(infra / total * 100)
        person['sci'] = round(sci / total * 100)

    data = {'full_list': full_list}
    print (data)

    return data


def create_list_single_legislator(model_id):
    full_list = []
    legislator_ids = []
    for legislator in model_id:
        # This next line will need to be edited when we implement Google API
        if legislator.type == 'sen':
            legislator_ids.append(legislator.lis_id)
            full_list.append({'id': legislator.lis_id,
                              'bioguide_id': legislator.bioguide_id,
                              'f_name': legislator.first_name,
                              'l_name': legislator.last_name,
                              'full_name': legislator.full_name,
                              'agg': 0, 'mil': 0, 'ed': 0, 'intl': 0, 'def': 0,
                              'energy': 0, 'health': 0, 'env': 0, 'infra': 0,
                              'sci': 0})
        # This next line will need to be edited when we implement Google AP
        elif legislator.district == 2:
            legislator_ids.append(legislator.bioguide_id)
            full_list.append({'id': legislator.bioguide_id,
                              'bioguide_id': legislator.bioguide_id,
                              'f_name': legislator.first_name,
                              'l_name': legislator.last_name,
                              'full_name': legislator.full_name,
                              'agg': 0, 'mil': 0, 'ed': 0, 'intl': 0, 'def': 0,
                              'energy': 0, 'health': 0, 'env': 0, 'infra': 0,
                              'sci': 0})

    # Get all votes where a user's legislator voted 'Yea'
    vote_model = TestVote.objects.all()
    votes = []
    bill_numbers = []
    for vote in vote_model:
        if vote.voter_id in legislator_ids and vote.value == 'Yea':
            bill_numbers.append(vote.number)
            votes.append(vote)

    # Get all bills/committees where a user's legislator voted 'Yea'
    bill_model = TestBill.objects.all()
    bills = []
    for bill in bill_model:
        if bill.number in bill_numbers:
            bills.append(bill)

    # Link categories go committee names
    agg_terms = ['Agriculture']
    mil_terms = ['Armed Services', 'Veterans\' Affairs']
    ed_terms = ['Education and Labor', 'Small Business',
                'Health, Education, Labor, and Pensions']
    intl_terms = ['Foreign Affairs', 'Foreign Relations']
    def_terms = ['Homeland Security', 'Intelligence', 'Judiciary',
                 'Narcotics Control']
    energy_terms = ['Energy and Commerce']
    health_terms = ['Education and Labor', 'Energy and Commerce', 'Aging',
                    'Finance']
    env_terms = ['Energy and Commerce', 'Natural Resources',
                 'Energy and Natural Resources',
                 'Environment and Public Works']
    infra_terms = ['Energy and Commerce', 'Transportation and Infrastructure',
                   'Banking, Housing, and Urban Affairs',
                   'Commerce, Science and Transportation']
    sci_terms = ['Science, Space, and Technology',
                 'Commerce, Science and Transportation']

    # Add points for each category based on votes and sponsorship
    for person in full_list:  # Iterate over each user's legislator
        id_num = person.get('id')
        for vote in votes:  # Iterate over shortened votes list
            vote_id = vote.voter_id
            if id_num == vote_id and vote.value == 'Yea':  # Check for an ID match and 'Yea' vote
                vote_num = vote.number
                for bill in bills:  # Iterate over shortened bills list
                    if vote_num == bill.number:  # Check that the 'Yea' vote matches the bill
                        committee = bill.committee
                        sponsor_bonus = 0  # Initialize sponsor bonus to 0
                        # Rearrange sponsor name to match order in full_list
                        last_first = bill.sponsor
                        sponsor_split = last_first.split(', ')
                        sponsor = f'{sponsor_split[1]} {sponsor_split[0]}'
                        # Change sponsor bonus if this legeslator is the sponsor
                        if sponsor == person.get('full_name'):
                            sponsor_bonus = 10
                        # Add value points to legislators category if bill aligns with that category
                        if committee in agg_terms:
                            score = person.get('agg')
                            person['agg'] = score + 1 + sponsor_bonus
                        if committee in mil_terms:
                            score = person.get('mil')
                            person['mil'] = score + 1 + sponsor_bonus
                        if committee in ed_terms:
                            score = person.get('ed')
                            person['ed'] = score + 1 + sponsor_bonus
                        if committee in intl_terms:
                            score = person.get('intl')
                            person['intl'] = score + 1 + sponsor_bonus
                        if committee in def_terms:
                            score = person.get('def')
                            person['def'] = score + 1 + sponsor_bonus
                        if committee in energy_terms:
                            score = person.get('energy')
                            person['energy'] = score + 1 + sponsor_bonus
                        if committee in health_terms:
                            score = person.get('health')
                            person['health'] = score + 1 + sponsor_bonus
                        if committee in env_terms:
                            score = person.get('env')
                            person['env'] = score + 1 + sponsor_bonus
                        if committee in infra_terms:
                            score = person.get('infra')
                            person['infra'] = score + 1 + sponsor_bonus
                        if committee in sci_terms:
                            score = person.get('sci')
                            person['sci'] = score + 1 + sponsor_bonus

    # Add points based on committee roll
    membership_model = Membership.objects.all()
    for person in full_list:  # Iterate over each user's legislator
        bioguide = person.get('bioguide_id')
        for membership in membership_model:
            if bioguide == membership.bioguide_id:  # Check for an ID match
                committee_id = membership.thomas_id
                rank = membership.rank
                # Add value points to legislators category based on their rank in the aligning committee
                if committee_id == 'HSVC' or committee_id == 'SPAG':
                    score = person.get('health')
                    person['health'] = score + (40 - rank)
                elif committee_id == 'SSVA' or committee_id == 'SSAS' \
                        or committee_id == 'HSVR' or committee_id == 'HSAS':
                    score = person.get('mil')
                    person['mil'] = score + (40 - rank)
                elif committee_id == 'SSSB' or committee_id == 'SSHR' \
                        or committee_id == 'HSSM' or committee_id == 'HSED':
                    score = person.get('ed')
                    person['ed'] = score + (40 - rank)
                elif committee_id == 'SSJU' or committee_id == 'SSGA' \
                        or committee_id == 'SLIN' or committee_id == 'SCNC' \
                        or committee_id == 'HSJU' or committee_id == 'HLIG' \
                        or committee_id == 'HSHM':
                    score = person.get('def')
                    person['def'] = score + (40 - rank)
                elif committee_id == 'SSFR' or committee_id == 'JCSE' \
                        or committee_id == 'HSFA':
                    score = person.get('intl')
                    person['intl'] = score + (40 - rank)
                elif committee_id == 'SSFI' or committee_id == 'SSCM' \
                        or committee_id == 'SSBK' or committee_id == 'JSEC' \
                        or committee_id == 'HSPW':
                    score = person.get('infra')
                    person['infra'] = score + (40 - rank)
                elif committee_id == 'SSEV' or committee_id == 'HSCN' \
                        or committee_id == 'HSII':
                    score = person.get('env')
                    person['env'] = score + (40 - rank)
                elif committee_id == 'SSEG' or committee_id == 'HSIF':
                    score = person.get('energy')
                    person['energy'] = score + (40 - rank)
                elif committee_id == 'SSCM' or committee_id == 'HSSY':
                    score = person.get('sci')
                    person['sci'] = score + (40 - rank)
                elif committee_id == 'SSAF' or committee_id == 'HSAG':
                    score = person.get('agg')
                    person['agg'] = score + (40 - rank)

    # Adjust category scores based on 100 point maximum
    for person in full_list:
        agg = person.get('agg')
        mil = person.get('mil')
        ed = person.get('ed')
        intl = person.get('intl')
        defen = person.get('def')
        energy = person.get('energy')
        health = person.get('health')
        env = person.get('env')
        infra = person.get('infra')
        sci = person.get('sci')

        total = agg + mil + ed + intl + defen + energy + health + env + infra + sci

        test_list = []

        person['agg'] = round(agg / total * 100)
        person['mil'] = round(mil / total * 100)
        person['ed'] = round(ed / total * 100)
        person['intl'] = round(intl / total * 100)
        person['def'] = round(defen / total * 100)
        person['energy'] = round(energy / total * 100)
        person['health'] = round(health / total * 100)
        person['env'] = round(env / total * 100)
        person['infra'] = round(infra / total * 100)
        person['sci'] = round(sci / total * 100)

        test_list.append({'military': person['agg']})
        test_list.append({'government': person['mil']})
        test_list.append({'education': person['ed']})
        test_list.append({'healthcare_and_medicare': person['intl']})
        test_list.append({'veteran_affairs': person['def']})
        test_list.append({'housing_and_labor': person['energy']})
        test_list.append({'international_affairs': person['health']})
        test_list.append({'energy_and_environment': person['env']})
        test_list.append({'Science': person['infra']})
        test_list.append({'transportation_and_infrastructure': person['sci']})
        test_list.append({'food_and_agricultur_value': 0})
        test_list.append({'socialsecurity_or_unemployment': 0})

    return test_list
