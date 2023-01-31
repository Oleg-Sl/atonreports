from django.contrib import admin
from .models import (User, ProductionCalendar, CallsPlan, Direction, Stage, Company, Deal, Activity, Phone)


# Register your models here.
admin.site.register(User)
admin.site.register(ProductionCalendar)
admin.site.register(CallsPlan)
admin.site.register(Direction)
admin.site.register(Stage)
admin.site.register(Company)
admin.site.register(Deal)
admin.site.register(Activity)
admin.site.register(Phone)
