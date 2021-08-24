from django.contrib import admin
from .models import Client, Project, FinancialRequest, Partner, Transaction

class ClientModelAdmin(admin.ModelAdmin):
    list_display = ('type', 'full_name', 'company_name', 'started_at', 'owner')


class ProjectModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'client', 'price', 'started_at', 'ended_at', 'status')


class FinancialRequestModelAdmin(admin.ModelAdmin):
    list_display = ('type', 'status', 'amount', 'address', 'requester', 'requested_at')


class TransactionModelAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'gross_amount', 'net_amount', 'payment_platform', 'financial_request')


class PartnerModelAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'owner')


admin.site.register(Client, ClientModelAdmin)
admin.site.register(Project, ProjectModelAdmin)
admin.site.register(FinancialRequest, FinancialRequestModelAdmin)
admin.site.register(Partner, PartnerModelAdmin)
admin.site.register(Transaction, TransactionModelAdmin)
