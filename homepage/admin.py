from django.contrib import admin
from .models import Lead
from django.http import HttpResponse
import csv
from django.utils.encoding import smart_str
import xlwt


def export_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=lead.csv'
    writer = csv.writer(response, dialect="excel", delimiter=' ')
    response.write(u'\ufeff'.encode('utf8'))
    writer.writerow([
        smart_str(u"date creation"),
        smart_str(u"nom"),
        smart_str(u"prenom"),
        smart_str(u"code postal"),
        smart_str(u"telephone"),
        smart_str(u"email"),
    ])
    for obj in queryset:
        writer.writerow([
            obj.date_creation,
            obj.nom,
            obj.prenom,
            smart_str(obj.code_postal),
            smart_str(obj.tel),
            obj.email,
        ])
    return response


def export_xls(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=lead.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Lead")

    row_num = 0

    columns = [
        (u"date", 4000),
        (u"nom", 4000),
        (u"prenom", 4000),
        (u"code postal", 4000),
        (u"telephone", 4000),
        (u"email", 6000),
    ]

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        # set column width
        ws.col(col_num).width = columns[col_num][1]

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1

    for obj in queryset:
        row_num += 1
        row = [
            smart_str(obj.date_creation),
            obj.nom,
            obj.prenom,
            obj.code_postal,
            obj.tel,
            obj.email,
        ]
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


export_xls.short_description = u"Export XLS"


def vendu(self, request, queryset):
    queryset.update(sold=True)


vendu.short_description = "vendu"

export_csv.short_description = u"Export CSV"


class LeadAdmin(admin.ModelAdmin):
    list_display = ('date_creation', 'sold', '__str__', 'code_postal', 'email', 'tel')
    date_hierarchy = 'date_creation'
    list_editable = ('sold',)
    list_filter = ['date_creation', 'sold', 'code_postal']
    ordering = ['sold']
    search_fields = ['nom', 'email', 'tel', 'code_postal']
    actions = [export_csv, vendu, export_xls, ]


admin.site.register(Lead, LeadAdmin)
