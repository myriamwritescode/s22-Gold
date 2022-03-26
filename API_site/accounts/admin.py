from django.contrib import admin

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



