from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .resources import *
from .models import *

admin.site.register(Customer)
admin.site.register(Representative)
admin.site.register(Represent)
admin.site.register(Bill)
# admin.site.register(Committee)
# admin.site.register(Committees)
admin.site.register(Sponsor)
admin.site.register(Sponsors)
admin.site.register(Votes)


# Test model for TestElectedOfficial --Brett
@admin.register(TestElectedOfficial)
class ElectedOfficialAdmin(ImportExportModelAdmin):
    resource_class = ElectedOfficialResource
    list_display = ['first_name', 'last_name', 'bioguide_id', 'lis_id', 'party',
                    'state', 'type', 'district']


# Test model for TestVotes --Brett
@admin.register(TestVote)
class VotesAdmin(ImportExportModelAdmin):
    resource_class = VotesResource
    list_display = ['voter_id', 'yr', 'bill_type', 'number', 'value', 'result']


# Test model for TestBills --Brett
@admin.register(TestBill)
class BillsAdmin(ImportExportModelAdmin):
    resource_class = BillsResource
    list_display = ['bill_tag', 'number', 'chamber', 'committee', 'sponsor']


# Test model for Committees --Brett
@admin.register(Committee)
class CommitteeAdmin(ImportExportModelAdmin):
    resource_class = CommitteesResource
    list_display = ['thomas_id', 'committee_id', 'chamber', 'name']


# Test model for Memberships --Brett
@admin.register(Membership)
class MembershipAdmin(ImportExportModelAdmin):
    resource_class = MembershipResource
    list_display = ['thomas_id', 'name', 'rank', 'bioguide_id']
