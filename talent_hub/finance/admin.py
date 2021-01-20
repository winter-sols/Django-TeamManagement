from django.contrib import admin
from .models import Client, Project, FinancialRequest, Partner, Transaction

admin.site.register(Client)
admin.site.register(Project)
admin.site.register(FinancialRequest)
admin.site.register(Partner)
admin.site.register(Transaction)
