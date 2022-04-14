from django.db import models
from django.contrib.auth.models import User
# from address.models import AddressField
# from django.utils.translation import ugettext_lazy as _
# from djmoney.models.fields import MoneyField
from django.core.validators import MinValueValidator, MaxValueValidator


# from .models.address import BaseBillingAddress
# from yamlfield.fields import YAMLField


# Test model for ElectedOfficial --Brett
class TestElectedOfficial(models.Model):
    last_name = models.CharField(max_length=100, null=True)
    first_name = models.CharField(max_length=100, null=True)
    middle_name = models.CharField(max_length=100, null=True)
    suffix = models.CharField(max_length=100, null=True)
    nickname = models.CharField(max_length=100, null=True)
    full_name = models.CharField(max_length=100, null=True)
    birthday = models.DateField(max_length=100, null=True)
    gender = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=100, null=True)  # rep or sen
    state = models.CharField(max_length=100, null=True)
    district = models.IntegerField(null=True)
    senate_class = models.IntegerField(null=True)
    party = models.CharField(max_length=100, null=True)
    url = models.CharField(max_length=250, null=True)
    address = models.CharField(max_length=250, null=True)
    phone = models.CharField(max_length=100, null=True)
    contact_form = models.CharField(max_length=250, null=True)
    rss_url = models.CharField(max_length=250, null=True)
    twitter = models.CharField(max_length=250, null=True)
    facebook = models.CharField(max_length=250, null=True)
    youtube = models.CharField(max_length=250, null=True)
    youtube_id = models.CharField(max_length=250, null=True)
    bioguide_id = models.CharField(max_length=250, primary_key=True, default=999)
    thomas_id = models.CharField(max_length=250, null=True)
    opensecrets_id = models.CharField(max_length=250, null=True)
    lis_id = models.CharField(max_length=250, null=True)
    fec_ids = models.CharField(max_length=250, null=True)
    cspan_id = models.CharField(max_length=250, null=True)
    govtrack_id = models.CharField(max_length=250, null=True)
    votesmart_id = models.CharField(max_length=250, null=True)
    ballotpedia_id = models.CharField(max_length=250, null=True)
    washington_post_id = models.CharField(max_length=250, null=True)
    icpsr_id = models.CharField(max_length=250, null=True)
    wikipedia_id = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


#  Test model for Votes --Brett
class TestVote(models.Model):
    voter_id = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    bill_type = models.CharField(max_length=100, null=True)
    number = models.IntegerField(null=True)
    roll = models.IntegerField(null=True)
    value = models.CharField(max_length=100, null=True)
    result = models.CharField(max_length=100, null=True)
    chamber = models.CharField(max_length=100, null=True)
    sess = models.IntegerField(null=True)
    yr = models.IntegerField(null=True)
    category = models.CharField(max_length=100, null=True)
    type_vote = models.CharField(max_length=100, null=True)
    # datetime = models.DateTimeField(null=True)
    # updated = models.DateTimeField(null=True)

    def __str__(self):
        return self.voter_id


#  Test model for Bills --Brett
class TestBill(models.Model):
    bill_tag = models.CharField(max_length=250, null=True)
    number = models.IntegerField(null=True)
    chamber = models.CharField(max_length=100, null=True)
    committee = models.CharField(max_length=100, null=True)
    sponsor = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.bill_tag + str(self.number)


class Customer(models.Model):
    # add this for the User profile create a one to one relationship (customer - User)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    Age = models.CharField("Age", max_length=3, null=True, )
    # address = AddressField(related_name='+', blank=True, null=True)
    number = models.CharField('Number', max_length=30, null=True, blank=True)
    street_line1 = models.CharField('Address 1', max_length=100, null=True, blank=True)
    street_line2 = models.CharField('Address 2', max_length=100, null=True, blank=True)
    zipcode = models.CharField('ZIP code', max_length=5, null=True, blank=True)
    city = models.CharField('City', max_length=100, null=True, blank=True)
    state = models.CharField('State', max_length=100, null=True, blank=True)
    # value score below
    agriculture = models.IntegerField(
                                      default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    military_and_veterans = models.IntegerField("Military and Veterans",
                                                default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    education_and_labor = models.IntegerField("Education and Labor",
                                              default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    international_affairs = models.IntegerField("International Affairs",
                                                default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    defense_and_intelligence = models.IntegerField("Defense and Intelligence",
                                                   default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    energy = models.IntegerField("Energy",
                                 default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    healthcare = models.IntegerField("Healthcare",
                                     default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    environment = models.IntegerField("Environment",
                                      default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    infrastructure = models.IntegerField("Infrastructure",
                                         default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    science = models.IntegerField("Science",
                                  default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    # military = models.IntegerField("Military", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    # government = models.IntegerField("Government", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    # education = models.IntegerField("Education", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    # healthcare_and_medicare = models.IntegerField("Healthcare and Medicare", default=0,
    #                                               validators=[MinValueValidator(0), MaxValueValidator(100)])
    # veteran_affairs = models.IntegerField("Veteran's Affairs", default=0,
    #                                       validators=[MinValueValidator(0), MaxValueValidator(100)])
    # housing_and_labor = models.IntegerField("Housing and Labor", default=0,
    #                                         validators=[MinValueValidator(0), MaxValueValidator(100)])
    # international_affairs = models.IntegerField("International Affairs", default=0,
    #                                             validators=[MinValueValidator(0), MaxValueValidator(100)])
    # energy_and_environment = models.IntegerField("Energy and Environment", default=0,
    #                                              validators=[MinValueValidator(0), MaxValueValidator(100)])
    # Science = models.IntegerField("Science", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    # transportation_and_infrastructure = models.IntegerField("Transportation and Infrastructure", default=0,
    #                                                         validators=[MinValueValidator(0), MaxValueValidator(100)])
    # food_and_agriculture = models.IntegerField("Food and Agriculture", default=0,
    #                                            validators=[MinValueValidator(0), MaxValueValidator(100)])
    # socialsecurity_or_unemployment = models.IntegerField("Social Security or Unemployment", default=0,
    #                                                      validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return self.name  # <----to see the name in not the id


# Table: REPRESENTATIVE
class Representative(models.Model):
    firstname = models.CharField("FirstName", max_length=200, null=True)
    lastname = models.CharField("LastName", max_length=200, null=True)
    gender = models.CharField("Gender", max_length=1, null=True, )
    birth_date = models.DateField('Date of Birth', null=True, blank=True)
    officeaddress = models.CharField("Office Address", max_length=1024, null=True, blank=True)
    # number = models.CharField(_('Number'), max_length = 30, null=True, blank = True)
    # street_line1 = models.CharField(_('Address 1'), max_length = 100, null=True, blank = True)
    # street_line2 = models.CharField(_('Address 2'), max_length = 100, null=True, blank = True)
    # zipcode = models.CharField(_('ZIP code'), max_length = 5, null=True, blank = True)
    # city = models.CharField(_('City'), max_length = 100, null=True, blank = True)
    state = models.CharField('State', max_length=100, null=True, blank=True)
    district = models.IntegerField("District", null=True, blank=True)
    phone = models.CharField("Phone", max_length=1024, null=True, blank=True)
    type = models.CharField("Type", max_length=1024, null=True, blank=True)
    # representativetown = models.CharField("Representative Town", max_length=1024)
    party = models.CharField("Party", max_length=1024, null=True, blank=True)
    # value score below
    military = models.IntegerField("Military", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    government = models.IntegerField("Government", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    education = models.IntegerField("Education", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    healthcare_and_medicare = models.IntegerField("Healthcare and Medicare", default=0,
                                                  validators=[MinValueValidator(0), MaxValueValidator(100)])
    veteran_affairs = models.IntegerField("Veteran's Affairs", default=0,
                                          validators=[MinValueValidator(0), MaxValueValidator(100)])
    housing_and_labor = models.IntegerField("Housing and Labor", default=0,
                                            validators=[MinValueValidator(0), MaxValueValidator(100)])
    international_affairs = models.IntegerField("International Affairs", default=0,
                                                validators=[MinValueValidator(0), MaxValueValidator(100)])
    energy_and_environment = models.IntegerField("Energy and Environment", default=0,
                                                 validators=[MinValueValidator(0), MaxValueValidator(100)])
    Science = models.IntegerField("Science", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    transportation_and_infrastructure = models.IntegerField("Transportation and Infrastructure", default=0,
                                                            validators=[MinValueValidator(0), MaxValueValidator(100)])
    food_and_agriculture = models.IntegerField("Food and Agriculture", default=0,
                                               validators=[MinValueValidator(0), MaxValueValidator(100)])
    socialsecurity_or_unemployment = models.IntegerField("Social Security or Unemployment", default=0,
                                                         validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return self.firstname + ' ' + self.lastname  # <----to see the name in not the id


# Table: REPRESENT
class Represent(models.Model):
    representative = models.ForeignKey(Representative, null=True, on_delete=models.SET_NULL)  # one to many relationship
    anonymous = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)  # one to many relationship
    # district =models.IntegerField("District", null=True, blank=True)
    state = models.CharField("State", max_length=1024, null=True, blank=True)
    servicescore = models.IntegerField("Service Score", null=True, blank=True)

    def __str__(self):
        return self.anonymous.name  # <----to see the name in not the id


# Table: BILL
class Bill(models.Model):
    number = models.CharField("Bill Number", max_length=200, null=True)
    date = models.DateField('Date', null=True, blank=True)
    outcome = models.CharField("Vote Result", max_length=200, null=True, blank=True)
    description = models.CharField("Description", max_length=1024, null=True, blank=True)
    # sRoll = models.CharField("Senate Vote Number", max_length=200, null=True, blank=True)
    sRoll = models.IntegerField("Senate Vote Number", null=True, blank=True)
    hrRoll = models.IntegerField("House Roll", null=True, blank=True)

    # hrRoll = models.CharField("House Roll", max_length=200, null=True, blank=True)

    def __str__(self):
        return self.number  # <----to see the name in not the id


# Table: Committee --Brett
class Committee(models.Model):
    chamber = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=200, null=True)
    thomas_id = models.CharField(max_length=100, null=True)
    committee_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


# Table: Membership --Brett
class Membership(models.Model):
    thomas_id = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=200, null=True)
    rank = models.IntegerField(null=True)
    bioguide_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


# # Table: Committees
# class Committees(models.Model):
#     committee = models.ForeignKey(Committee, null=True, on_delete=models.SET_NULL)  # one to many relationship
#     bill = models.ForeignKey(Bill, null=True, on_delete=models.SET_NULL)  # one to many relationship
#
#     def __str__(self):
#         return self.bill.number + ' ' + self.committee.category  # <----to see the name in not the id


# Table: Sponsor
class Sponsor(models.Model):
    # name = models.CharField("Name", max_length=250, null=True)
    lastname = models.CharField("LastName", max_length=200, null=True)
    firstname = models.CharField("FirstName", max_length=200, null=True)

    def __str__(self):
        return self.firstname + ' ' + self.lastname  # <----to see the name in not the id


# Table: Sponsors
class Sponsors(models.Model):
    sponsor = models.ForeignKey(Sponsor, null=True, on_delete=models.SET_NULL)  # one to many relationship
    bill = models.ForeignKey(Bill, null=True, on_delete=models.SET_NULL)  # one to many relationship

    def __str__(self):
        # to see the name in not the id
        return self.bill.number + ' ' + self.sponsor.firstname + ' ' + self.sponsor.lastname


# Table: VOTES
class Votes(models.Model):
    # BillNumber = models.CharField("BillNumber", max_length=200, null=True)
    roll = models.IntegerField("Roll", null=True, blank=True)
    date = models.DateField('Date', null=True, blank=True)
    voteCast = models.CharField("Vote Cast", max_length=3, null=True)
    representative = models.ForeignKey(Representative, null=True, on_delete=models.SET_NULL)  # one to many relationship
    vote = models.ForeignKey(Bill, null=True, on_delete=models.SET_NULL)  # one to many relationship

    def __str__(self):
        # to see the name in not the id
        return self.vote.number + ' ' + self.representative.firstname + ' ' + self.representative.lastname

#  TEST AREA
