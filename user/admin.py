from django.contrib import admin

from place.models import wishist
from user.models import UserProfile

# Register your models here.
#<editor-fold desc="userprofile Admin">
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'lang', 'phone', 'city', 'image_tag', ]
    list_filter = ['city', 'country', ]
#</editor-fold

admin.site.register(UserProfile, UserProfileAdmin)

