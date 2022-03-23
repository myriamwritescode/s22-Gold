from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Customer)
# AnonymousUser
admin.site.register(AnonymousUser)
#  Representative
admin.site.register(Representative)
admin.site.register(Represent)
admin.site.register(Education)
admin.site.register(AllEducation)
admin.site.register(Experience)
admin.site.register(AllExperience)
admin.site.register(Vote)
admin.site.register(AllVote)
admin.site.register(Sponsor)
admin.site.register(AllSponsor)
admin.site.register(Sector)
admin.site.register(AllSector)

