
# Register your models here.
from django.contrib import admin
from .models import *
# Register your models here.
# class CustomAdminSite(admin):
#     site_header = 'Zishan Backend'
#     site_title = 'Backend'
#     index_title = 'Databases'

# custom_admin_site = CustomAdminSite(name='custom_admin')
admin.site.register(Book)