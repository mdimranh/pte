from django.contrib import admin

from .models import Group, Plan, Profile, Purchase, OrganizationPackage

admin.site.register(Profile)
admin.site.register(Plan)
admin.site.register(Purchase)
admin.site.register(Group)
admin.site.register(OrganizationPackage)
