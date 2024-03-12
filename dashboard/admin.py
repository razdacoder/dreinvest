from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, Transaction, Proof

# Register your models here.


admin.site.register(User)
admin.site.register(Transaction)
admin.site.register(Proof)
admin.site.unregister(Group)
