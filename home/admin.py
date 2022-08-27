from django.contrib import admin
from home.models import Language, Setting, ContactMessage, SettingLang, Faq, FaqLanguage
# Register your models here.
#<editor-fold desc="Language Admin">
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'status']
    list_filter = ['status']
#</editor-fold >
#<editor-fold desc="Setting and SettingLanguage Admin">
class SettingSettingLanguageInline(admin.TabularInline):
    model = SettingLang
    extra = 1
class SettingAdmin(admin.ModelAdmin):
    list_display = ['title', 'description','fax','phone','email','status']
    list_filter = ['status']
    inlines = [SettingSettingLanguageInline,]
class SettingLanguageAdmin(admin.ModelAdmin):
    list_display = ['title', 'keyword', 'description', 'lang']
    list_filter = ['lang']
#</editor-fold >
#<editor-fold desc="Faq and FaqLanguage Admin">
class FaqFaqLanguageInline(admin.TabularInline):
    model = FaqLanguage
    extra = 1
class FaqAdmin(admin.ModelAdmin):
    list_display = ['ordered','question', 'answer','status']
    list_filter = ['status',]
    inlines=[FaqFaqLanguageInline,]
class FaqLanguageAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'lang',]
    list_filter = ['lang',]
#</editor-fold >
#<editor-fold desc="Contact Message Admin">
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject','status']
    readonly_fields = ('name','ip','message','subject','email',)
    list_filter = ['status']
#</editor-fold >
#<editor-fold desc="Admin.site.register for Home">
admin.site.register(Language,LanguageAdmin)
admin.site.register(Setting,SettingAdmin)
admin.site.register(SettingLang,SettingLanguageAdmin)
admin.site.register(Faq,FaqAdmin)
admin.site.register(FaqLanguage,FaqLanguageAdmin)
admin.site.register(ContactMessage,ContactMessageAdmin)
#</editor-fold>