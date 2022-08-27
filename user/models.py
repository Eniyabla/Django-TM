from django.contrib.auth.models import User
from django.db import models
from home.models import Language
# Create your models here.
from django.utils.safestring import mark_safe
#<editor-fold desc="UserProfile Model">
from place.models import Place


class UserProfile(models.Model):
    lang=models.ForeignKey(Language, on_delete=models.CASCADE,blank=True,null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(blank=True, max_length=25)
    address = models.CharField(blank=True, max_length=255)
    city = models.CharField(blank=True, max_length=25)
    country = models.CharField(blank=True, max_length=25)
    image = models.ImageField(blank=True, upload_to='images/user')
    def __str__(self):
        return self.user.username
    def user_name(self):
        return self.user.first_name + ' ' + self.user.last_name + ' [' + self.user.username + ']'

    def image_tag(self):
        return mark_safe('<img src="{}" width="30" height="30" style="border-radius:50%" />'.format(self.image.url))

    image_tag.short_description = 'Image'

#</editor-fold>
#<editor-fold desc="Wishlist Model" >