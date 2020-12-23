from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import User, Profile, Account, AccountSecurityQA

class MyCustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )

admin.site.register(User, MyCustomUserAdmin)
admin.site.register(Profile)
admin.site.register(Account)
admin.site.register(AccountSecurityQA)
admin.site.unregister(Group)