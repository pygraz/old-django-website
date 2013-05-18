from django.contrib import admin

from . import models


class CompanyAdmin(admin.ModelAdmin):
    model = models.Company
    raw_id_fields = ['editors']
    list_display = ('name', 'approved')


admin.site.register(models.Company, CompanyAdmin)