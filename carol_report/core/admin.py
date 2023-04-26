import csv
from decimal import Decimal

from django.contrib import admin
from django.http import HttpResponse
from core.models import File, Status, Company, Product, Lines, LogLineError

# Register your models here.

class ExportCSV:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            row = [str(getattr(obj, field)).replace('.', ',') if isinstance(getattr(obj, field), Decimal) else getattr(obj, field) for field in field_names]
            writer.writerow(row)
        return response

    export_as_csv.short_description = "Exportar-CSV"


class LinesAdmin(admin.ModelAdmin, ExportCSV):
    list_display = ['reference', 'status', 'client', 'product', 'date_create', 'date_confirm', 'profit', 'transfer_fee_amount', 'result']
    search_fields = ['reference',]
    actions = ['export_as_csv']

    
admin.site.register(File)
admin.site.register(Status)
admin.site.register(Company)
admin.site.register(Product)
admin.site.register(Lines, LinesAdmin)
admin.site.register(LogLineError)