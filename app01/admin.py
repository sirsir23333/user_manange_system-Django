from django.contrib import admin

# Register your models here.
from .models import User


# register User Model into the admin site interface
# I customized User Model, which can be seen in models.py

class UserProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserProfileAdmin)


# By defining this class and registering it with the Django admin site,
# you can customize how the user profile model is displayed and edited in the Django admin interface.
