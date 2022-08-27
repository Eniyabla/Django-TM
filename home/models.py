from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
#<editor-fold desc="Language Model">
from django.forms import ModelForm, TextInput, Textarea


class Language(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=5)
    status = models.BooleanField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
llist = Language.objects.filter(status=True)
list1 = []
for elt in llist:
    list1.append((elt.code, elt.name))
langlist = (list1)

#</editor-fold desc="Language Model">
#<editor-fold desc="Setting Model">
class Setting(models.Model):

    title = models.CharField(max_length=30, blank=True)
    keyword = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)
    facebook = models.CharField(max_length=255, blank=True)
    twitter = models.CharField(max_length=255, blank=True)
    instagram = models.CharField(max_length=255, blank=True)
    youtube = models.CharField(max_length=255, blank=True)
    linkedin = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    fax = models.CharField(max_length=255, blank=True)
    contact = RichTextUploadingField(blank=True)
    about = RichTextUploadingField(blank=True)
    reference = RichTextUploadingField(blank=True)
    status = models.BooleanField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
class SettingLang(models.Model):
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE)
    lang = models.CharField(max_length=6, choices=langlist, blank=True, null=True)
    title = models.CharField(max_length=30, blank=True)
    keyword = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)
    contact = RichTextUploadingField(blank=True)
    about = RichTextUploadingField(blank=True)
    reference = RichTextUploadingField(blank=True)


    def __str__(self):
        return self.title

#</editor-fold desc="Setting Model">
#<editor-fold desc="Contact Message Model">
class ContactMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )
    status = models.CharField(max_length=10, choices=STATUS)
    name = models.CharField(blank=True, max_length=30)
    email = models.CharField(blank=True, max_length=30)
    subject = models.CharField(blank=True, max_length=30)
    message = models.TextField()
    ip = models.CharField(max_length=30)
    note = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
#</editor-fold desc="Contact Message Model">
#<editor-fold desc="Contact Form Model">
class ContactForm(ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': TextInput(attrs={'class': 'input', 'placeholder': 'Full Name'}),
            'subject': TextInput(attrs={'class': 'input', 'placeholder': 'subject'}),
            'email': TextInput(attrs={'class': 'input', 'placeholder': 'Your email'}),
            'message': Textarea(attrs={'class': 'input', 'placeholder': 'Your Message'}),

        }
#</editor-fold desc="Contact Form Model">
#<editor-fold desc="Contact Faq and FaqLanguage Models">
class Faq(models.Model):
    ordered = models.IntegerField()
    status = models.BooleanField()
    question = models.CharField(blank=True, max_length=250)
    answer = RichTextUploadingField(blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
class FaqLanguage(models.Model):
    lang = models.CharField(max_length=6, choices=langlist, blank=True, null=True)
    faq = models.ForeignKey(Faq, on_delete=models.CASCADE)
    question = models.CharField(blank=True, max_length=250)
    answer = RichTextUploadingField(blank=True)
#</editor-fold>