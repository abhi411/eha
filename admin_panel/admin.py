from django.contrib import admin

from .models import *

# MODEL : AdminUser
class AdminUserClass(admin.ModelAdmin):
	list_display = ('id','username','password')
admin.site.register(AdminUser ,AdminUserClass)
