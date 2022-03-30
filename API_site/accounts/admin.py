from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .resources import *

# Register your models here.
from .models import *

admin.site.register(Customer)
#  Representative
admin.site.register(Representative)
admin.site.register(Represent)
admin.site.register(Bill)
admin.site.register(Committee)
admin.site.register(Committees)
admin.site.register(Sponsor)
admin.site.register(Sponsors)
admin.site.register(Votes)




# Test model for TestElectedOfficial --Brett
@admin.register(TestElectedOfficial)
class ElectedOfficialAdmin(ImportExportModelAdmin):
    resource_class = ElectedOfficialResource
    list_display = ['bioguide_id', 'first_name', 'last_name', 'party', 'state',
                    'type', 'district']


# Test model for TestVotes --Brett
@admin.register(TestVote)
class VotesAdmin(ImportExportModelAdmin):
    resource_class = VotesResource
    list_display = ['voter_id', 'yr', 'bill_type', 'number', 'value', 'result']


# Test model for TestBills --Brett
@admin.register(TestBill)
class BillsAdmin(ImportExportModelAdmin):
    resource_class = BillsResource
    list_display = ['bill_id', 'sponsor_1', 'sponsor_2', 'sponsor_3',
                    'committee_1', 'committee_2', 'committee_3']
