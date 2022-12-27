from django.contrib import admin
from .models import *


class AccountsAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name', 'balance', 'user', 'city')


admin.site.register(BankAccount, AccountsAdmin)
