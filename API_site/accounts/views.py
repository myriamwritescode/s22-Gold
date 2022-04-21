'''

this handles the response and render for all request for this application

'''

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm  # <---django forms for authentication
from django.contrib.auth import authenticate, login, logout  # <---authentication
from django.contrib import messages  # <---this for flash messages: one-time message send to the template
from django.contrib.auth.decorators import login_required  # <---for every view that need to be restriction
from django.contrib.auth.models import Group
from django.urls import reverse
from django.http import JsonResponse
# from ..scratch_1 import servicecalculator
import numpy as NP
import math
# Create your views here for the path response

# make get requests to google civic api and get json reponse
import requests
import json

from .models import *
from .forms import CreateUserForm, CustomerForm, FeedbackForm  # we need to import to pass it to the template
# from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only  # permission


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


# --------------------------------------------------------------------------Feedback page
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def feedbackpage(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('feedback-thanks')
    else:
        form = FeedbackForm()
    context = {'form': form}
    return render(request, 'accounts/feedback.html', context)


# --------------------------------------------------------------------------Feedback page
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'admin'])
def feedbackpageThanks(request):
    return render(request, 'accounts/feedbackThanks.html')


# --------------------------------------------------------------------------User comaper home page
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'admin'])
def comparePage(request):
    return render(request, 'accounts/compareCommunity.html')


# --------------------------------------------------------------------------User value page
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'admin'])
def valuePage(request):
    # Create a list of the user's legislator's ids
    if hasattr(request.user, 'customer'):
        current_user = request.user.customer

        if current_user.district is None:
            print('ACCESSING IF STATEMENT')
            with open("representatives.json") as rep:
                data = json.load(rep)
                current_user.district = data['offices'][0]['divisionId'][-1]
                current_user.save()

        user_state = current_user.state
        user_district = current_user.district
    else:
        user_state = 'VA'
        user_district = 2

    print('FIND USER STATE HERE: ')
    print(user_state)
    print('FIND USER DISTRICT HERE: ')
    print(user_district)

    legislator_model = TestElectedOfficial.objects.filter(state__exact=user_state)
    data = create_dict_multi_legislators(legislator_model, user_district)

    return render(request, 'accounts/value.html', data)


# -------------------------------------------------------Graphing the result Data
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'admin'])
def resultsDatalegislative(request, pk_test):
    votedata = []  # built and empty array
    votedata_legislative = []
    alldata = []
    if hasattr(request.user, 'customer'):
        current_user = request.user.customer
        user_district = current_user.district
        constituent = request.user.customer  # grab the by the ID of the model
        print("constituent")
        votedata.append({'agriculture': constituent.agriculture})
        votedata.append({'military_and_veterans': constituent.military_and_veterans})
        votedata.append({'education_and_labor': constituent.education_and_labor})
        votedata.append({'international_affairs': constituent.international_affairs})
        votedata.append({'defense_and_intelligence': constituent.defense_and_intelligence})
        votedata.append({'energy': constituent.energy})
        votedata.append({'healthcare': constituent.healthcare})
        votedata.append({'environment': constituent.environment})
        votedata.append({'infrastructure': constituent.infrastructure})
        votedata.append({'science': constituent.science})

        alldata.append(votedata)
    else:
        user_district = 2
        legislator_model = TestElectedOfficial.objects.filter(bioguide_id='W000805')
        votedata = create_list_single_legislator(legislator_model, user_district)
        alldata.append(votedata)
        print("legislative")

    # grab the by the ID of the model
    legislative_model = TestElectedOfficial.objects.filter(bioguide_id=pk_test)

    votedata_legislative = create_list_single_legislator(legislative_model, user_district)

    alldata.append(votedata_legislative)

    return JsonResponse(alldata, safe=False)  # send it to the javascript


# --------------------------------------------------------------------------User value learn more page


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'admin'])
def valuePagelearnmore(request, pk_test):
    user_score = []
    legislative_score = []

    if hasattr(request.user, 'customer'):
        current_user = request.user.customer
        user_district = current_user.district
        constituent = request.user.customer  # grab the by the ID of the model
        user_score.append(constituent.agriculture)
        user_score.append(constituent.military_and_veterans)
        user_score.append(constituent.education_and_labor)
        user_score.append(constituent.international_affairs)
        user_score.append(constituent.defense_and_intelligence)
        user_score.append(constituent.energy)
        user_score.append(constituent.healthcare)
        user_score.append(constituent.environment)
        user_score.append(constituent.infrastructure)
        user_score.append(constituent.science)
    else:
        # constituent = TestElectedOfficial.objects.get(bioguide_id='W000805')
        user_district = 2
        # Create a list of the user's legislator's ids
        legislator_model = TestElectedOfficial.objects.filter(bioguide_id='W000805')
        votedata_legislative = create_list_single_legislator(legislator_model, user_district)
        user_score.append(votedata_legislative[0]['agriculture'])
        user_score.append(votedata_legislative[1]['military_and_veterans'])
        user_score.append(votedata_legislative[2]['education_and_labor'])
        user_score.append(votedata_legislative[3]['international_affairs'])
        user_score.append(votedata_legislative[4]['defense_and_intelligence'])
        user_score.append(votedata_legislative[5]['energy'])
        user_score.append(votedata_legislative[6]['healthcare'])
        user_score.append(votedata_legislative[7]['environment'])
        user_score.append(votedata_legislative[8]['infrastructure'])
        user_score.append(votedata_legislative[9]['science'])

    # grab the by the ID of the model
    # legislative = TestElectedOfficial.objects.get(bioguide_id=pk_test)

    legislator_model = TestElectedOfficial.objects.filter(bioguide_id=pk_test)
    legislator_vote_date = create_list_single_legislator(legislator_model, user_district)
    legislative_score.append(legislator_vote_date[0]['agriculture'])
    legislative_score.append(legislator_vote_date[1]['military_and_veterans'])
    legislative_score.append(legislator_vote_date[2]['education_and_labor'])
    legislative_score.append(legislator_vote_date[3]['international_affairs'])
    legislative_score.append(legislator_vote_date[4]['defense_and_intelligence'])
    legislative_score.append(legislator_vote_date[5]['energy'])
    legislative_score.append(legislator_vote_date[6]['healthcare'])
    legislative_score.append(legislator_vote_date[7]['environment'])
    legislative_score.append(legislator_vote_date[8]['infrastructure'])
    legislative_score.append(legislator_vote_date[9]['science'])

    legislative = TestElectedOfficial.objects.get(bioguide_id=pk_test)
    service_vector = NP.subtract(user_score, legislative_score)

    # find magnitude of the resulting vector
    servicescore = math.sqrt(sum(pow(element, 2) for element in
                                 service_vector))

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
    # check to see if true
    if request.method == 'POST':

        # access address passed in via POST request
        street_addr = request.POST.get('street_line1')
        city = request.POST.get('city')
        state = request.POST.get('state')

        # url pieces and parsing
        url_head = "https://civicinfo.googleapis.com/civicinfo/v2/representatives?address="
        # senator_url = "&includeOffices=true&levels=country&roles=legislatorUpperBody&key=AIzaSyA2yJqqdsAUV33ryKp50gq5Njs4UC6o3bc"
        representative_url = "&includeOffices=true&levels=country&roles=legislatorLowerBody&key=AIzaSyA2yJqqdsAUV33ryKp50gq5Njs4UC6o3bc"

        # formatting address info into url arguments
        cat_address_compnents = street_addr + " " + city + " " + state
        address = cat_address_compnents.replace(" ", "%20")

        # prepare request for senator info and write to a json
        # senator = url_head + address + senator_url
        # sen_response = requests.get(senator).text
        # with open("senators.json", "w", encoding="utf-8") as senator_file:
        #     senator_file.write(sen_response)

        # prepare request for representative info and write to a json
        representative = url_head + address + representative_url
        rep_response = requests.get(representative).text
        with open("representatives.json", "w", encoding="utf-8") as rep_file:
            rep_file.write(rep_response)

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
            form.science_and_technology = request.POST.get('science')

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
            sum += int(request.POST.get('science'))

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
        votedata.append({'agriculture': constituent.agriculture})
        votedata.append({'military_and_veterans': constituent.military_and_veterans})
        votedata.append({'education_and_labor': constituent.education_and_labor})
        votedata.append({'international_affairs': constituent.international_affairs})
        votedata.append({'defense_and_intelligence': constituent.defense_and_intelligence})
        votedata.append({'energy': constituent.energy})
        votedata.append({'healthcare': constituent.healthcare})
        votedata.append({'environment': constituent.environment})
        votedata.append({'infrastructure': constituent.infrastructure})
        votedata.append({'science': constituent.science})
    else:
        # Create a list of the user's legislator's ids
        user_district = 2
        legislator_model = TestElectedOfficial.objects.filter(bioguide_id='W000805')
        votedata = create_list_single_legislator(legislator_model, user_district)

    return JsonResponse(votedata, safe=False)


# -------------------------------------------------------Graphing the result Data
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'admin'])
def resultsDatalegislativeMulti(request):
    votedata = []  # built and empty array
    alldata = []
    legislators_name = []
    if hasattr(request.user, 'customer'):
        current_user = request.user.customer
        user_district = current_user.district
        constituent = request.user.customer  # grab the by the ID of the model
        print("constituent")
        votedata.append({'agriculture': constituent.agriculture})
        votedata.append({'military_and_veterans': constituent.military_and_veterans})
        votedata.append({'education_and_labor': constituent.education_and_labor})
        votedata.append({'international_affairs': constituent.international_affairs})
        votedata.append({'defense_and_intelligence': constituent.defense_and_intelligence})
        votedata.append({'energy': constituent.energy})
        votedata.append({'healthcare': constituent.healthcare})
        votedata.append({'environment': constituent.environment})
        votedata.append({'infrastructure': constituent.infrastructure})
        votedata.append({'science': constituent.science})
    else:
        # constituent = TestElectedOfficial.objects.get(bioguide_id='W000805')
        user_district = 2
        legislator_model = TestElectedOfficial.objects.filter(bioguide_id='W000805')
        votedata = create_list_single_legislator(legislator_model, user_district)
        # alldata.append(votedata)
        print("legislative")
    # add legislative
    # get all 3 bioguide_ids 
    # for each bioguide_id return list of value scores using create_single...

    if hasattr(request.user, 'customer'):
        current_user = request.user.customer
        if current_user.district is None:
            with open("representatives.json") as rep:
                data = json.load(rep)
                current_user.district = data['offices'][0]['divisionId'][-1]
                current_user.save()
        user_state = current_user.state
        user_district = current_user.district
    else:
        user_state = 'VA'
        user_district = 2

    legislators_model = TestElectedOfficial.objects.filter(state__exact=user_state)
    data = create_dict_multi_legislators(legislators_model, user_district)
    all_id = []
    for i in range(3):
        try:
            all_id.append(data['full_list'][i]['bioguide_id'])
            print(data['full_list'][i]['bioguide_id'])
            legislators_name.append({data['full_list'][i]['full_name']: 0})
            print({data['full_list'][i]['full_name']: 0})
            print('FOR i TRY EXECUTED')
        except IndexError:
            break

    for i in range(7):
        legislators_name.append({'name': 0})
        print({'name': 0})

    alldata.append(votedata)

    for i in all_id:
        legislator_model = TestElectedOfficial.objects.filter(bioguide_id=i)
        votedata_legislative = create_list_single_legislator(legislator_model, user_district)
        alldata.append(votedata_legislative)

    alldata.append(legislators_name)

    return JsonResponse(alldata, safe=False)


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
        print("constituent")
        votedata.append({'agriculture': constituent.agriculture})
        votedata.append({'military_and_veterans': constituent.military_and_veterans})
        votedata.append({'education_and_labor': constituent.education_and_labor})
        votedata.append({'international_affairs': constituent.international_affairs})
        votedata.append({'defense_and_intelligence': constituent.defense_and_intelligence})
        votedata.append({'energy': constituent.energy})
        votedata.append({'healthcare': constituent.healthcare})
        votedata.append({'environment': constituent.environment})
        votedata.append({'infrastructure': constituent.infrastructure})
        votedata.append({'science': constituent.science})

        total_demographics = Customer.objects.all().filter(Age=constituent.Age).count()
        myfilter = Customer.objects.all().filter(Age=constituent.Age)
    else:
        legislator_model = TestElectedOfficial.objects.filter(bioguide_id='W000805')
        votedata = create_list_single_legislator(legislator_model, 2)
        myfilter = Customer.objects.all()
        total_demographics = Customer.objects.all().count()
        print("legislative")

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
        demographics_science_and_technology_value += i.science

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
    votedata_demographics.append({'science': demographics_science_and_technology_value})

    # the construct the list that need to be graph
    alldata.append(votedata)
    alldata.append(votedata_demographics)

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
    legislative = TestElectedOfficial.objects.get(bioguide_id=pk_test)

    return render(request, 'accounts/bio.html', {'representative': legislative})


# ---------------------------------------------------------------------------------

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'admin'])
def votes(request, pk_test):
    legislative = TestElectedOfficial.objects.get(bioguide_id=pk_test)
    if (legislative.lis_id):
        votes = TestVote.objects.filter(voter_id=legislative.lis_id)
    else:
        votes = TestVote.objects.filter(voter_id=legislative.bioguide_id)

    return render(request, 'accounts/votes.html', {'votes': votes, 'representative': legislative})


# ---------------------------------------------------------------------------------

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'admin'])
def funding(request, pk_test):
    legislative = TestElectedOfficial.objects.get(bioguide_id=pk_test)

    return render(request, 'accounts/funding.html', {'representative': legislative})


# ---------------------------------------------------------------------------------


def create_dict_multi_legislators(model_id, user_district):
    full_list = []
    legislator_ids = []

    for legislator in model_id:
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
        elif legislator.district == user_district:
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

    return data


def create_list_single_legislator(model_id, user_district):
    full_list = []
    legislator_ids = []
    for legislator in model_id:
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
        elif legislator.district == user_district:
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

        test_list.append({'agriculture': person['agg']})
        test_list.append({'military_and_veterans': person['mil']})
        test_list.append({'education_and_labor': person['ed']})
        test_list.append({'international_affairs': person['intl']})
        test_list.append({'defense_and_intelligence': person['def']})
        test_list.append({'energy': person['energy']})
        test_list.append({'healthcare': person['health']})
        test_list.append({'environment': person['env']})
        test_list.append({'infrastructure': person['infra']})
        test_list.append({'science': person['sci']})

    return test_list
