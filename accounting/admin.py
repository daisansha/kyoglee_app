from django.contrib import admin
#from .models import ExpenseApplication

from accounting.models.expense_models import ExpenseApplication
from accounting.models.collection_models import Collection, CollectionRecord

admin.site.register(ExpenseApplication)
admin.site.register(Collection)
admin.site.register(CollectionRecord)