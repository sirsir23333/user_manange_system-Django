from django.contrib import admin

# Register your models here.
from .models import User


# register User Model into the admin site interface
# I customized User Model, which can be seen in models.py

class UserProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserProfileAdmin)
