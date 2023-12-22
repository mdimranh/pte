from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import fields, resources
from .models import ReadAloud

class ReadAloudResource(resources.ModelResource):
    class Meta:
        model = ReadAloud

class ReadAloudAdmin(ImportExportModelAdmin):
    resource_classes = [ReadAloudResource]

admin.site.register(ReadAloud, ReadAloudAdmin)
