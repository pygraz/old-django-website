from django.contrib import admin

from guardian.admin import GuardedModelAdmin

from . import models


class CompanyAdmin(GuardedModelAdmin):
    model = models.Company
    raw_id_fields = ['editors']
    list_display = ('name', 'approved')


admin.site.register(models.Company, CompanyAdmin)