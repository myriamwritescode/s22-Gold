from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Customer)
#  Representative
admin.site.register(Representative)
admin.site.register(Represent)
admin.site.register(Bill)
admin.site.register(Votes)

