from django.contrib import admin
from financials.models import Category, Transaction, Account, Budget

# Register your models here.
admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(Account)
admin.site.register(Budget)
