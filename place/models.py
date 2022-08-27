from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm, TextInput
from django.utils.safestring import mark_safe
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse
# import this
from home.models import Language
llist = Language.objects.filter(status=True)
list1 = []
for elt in llist:
    list1.append((elt.code, elt.name))
langlist = (list1)

#<editor-fold desc="Category Model">
class Category(MPTTModel):

    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    keyword = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.BooleanField()
    slug = models.SlugField(null=False, unique=True)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return '->'.join(full_path[::-1])
class CategoryLanguage(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    lang=models.CharField(max_length=6,choices=langlist,blank=True,null=True)
    title = models.CharField(max_length=30)
    keyword = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    slug = models.SlugField(null=False, unique=True)
    def get_absolute_url(self):
        return reverse('categorylang_detail', kwargs={'slug': self.slug})

#</editor-fold >
#<editor-fold desc="Place PlaceLanguage and Image Models">
class Place(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=30)
    keyword = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.BooleanField()
    slug = models.SlugField(null=False, unique=True)
    city = models.CharField(max_length=50, blank=True)
    detail = RichTextUploadingField(blank=True)
    country = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=50, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" width="50" height="50" />'.format(self.image.url))

    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('place_detail', kwargs={'slug': self.slug})
class PlaceForm(ModelForm):
    class Meta:
        model = Place
        fields = ['category', 'title', 'keyword', 'description', 'city', 'country', 'location', 'image', 'detail',
                  'status', ]
        widgets = {
            'title': TextInput(attrs={'class': 'input', 'placeholder': 'Title'}),
            'keyword': TextInput(attrs={'class': 'input', 'placeholder': 'keyword'}),
            'description': TextInput(attrs={'class': 'input', 'placeholder': 'Your description'}),
            'city': TextInput(attrs={'class': 'input', 'placeholder': 'City'}),
            'location': TextInput(attrs={'class': 'input', 'placeholder': 'location'}),
            'country': TextInput(attrs={'class': 'input', 'placeholder': 'Country'}),
        }

class PlaceLanguage(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    lang=models.CharField(max_length=6,choices=langlist,blank=True,null=True)
    title = models.CharField(max_length=30)
    keyword = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    slug = models.SlugField(null=False, unique=True)
    detail=RichTextUploadingField(blank=True,null=True)
    def get_absolute_url(self):
        return reverse('placelang_detail', kwargs={'slug': self.slug})

class Images(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title


class ImageForm(ModelForm):
    class Meta:
        model = Images
        fields = ['title', 'image']


#</editor-fold >
#<editor-fold desc="Comment Model" >
class Comment(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
        ('New', 'New'),
    )
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    comment = models.CharField(max_length=250)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=30)
    status = models.CharField(max_length=10, choices=STATUS, default='False')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']
#</editor-fold >