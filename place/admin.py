from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from home.models import Language
from place.models import Category, Place, CategoryLanguage, Images, PlaceLanguage, Comment, wishist

# Register your models here.
#<editor-fold desc="Category and CategoryLanguage Admin">

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent', 'status']
    list_filter = ['status']
class CategoryLanguageAdmin(admin.ModelAdmin):
    list_display = ['title', 'lang','slug',]
    list_filter = ['lang']
    prepopulated_fields = {'slug': ('title',) }

class CategoryLanguageInline(admin.TabularInline):
    model = CategoryLanguage
    extra = Language.objects.all().count()-1
    show_change_link = True
    prepopulated_fields = {'slug': ('title',)}



class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [CategoryLanguageInline,]

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
            qs,
            Place,
            'category',
            'products_cumulative_count',
            cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                                                Place,
                                                'category',
                                                'products_count',
                                                cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'

#</editor-fold >
#<editor-fold desc="Comment Admin">
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user','place','subject', 'rate', 'status','create_at']
    list_filter = ['status',]
    readonly_fields = ['comment','subject','ip','user','place','email','rate']
#</editor-fold>
#<editor-fold desc=". Admin">

#</editor-fold>
#<editor-fold desc="Place and PlaceLanguage Admin">

class PlaceImageInline(admin.TabularInline):
    model = Images
    extra = 5
class PlaceLanguageInline(admin.TabularInline):
    model=PlaceLanguage
    extra = 3
    show_change_link = True
    prepopulated_fields = {'slug': ('title',)}


class PlaceAdmin(admin.ModelAdmin):
    list_display = ['title', 'category','image_tag', 'status',]
    list_filter = ['category']
    readonly_fields = ['image_tag']
    inlines = [PlaceImageInline,PlaceLanguageInline]
    prepopulated_fields = {'slug': ('title',) }
class PlaceLanguageAdmin(admin.ModelAdmin):
    list_display = ['title', 'lang','slug',]
    list_filter = ['lang']
    prepopulated_fields = {'slug': ('title',) }
#</editor-fold >

#<editor-fold desc="Wishlist Admin">
class wishistAdmin(admin.ModelAdmin):
    list_display = ['place', 'user','isLike']
    readonly_fields = ['place', 'user','isLike']
#</editor-fold
#<editor-fold desc="Admin.site.register">
admin.site.register(Category, CategoryAdmin2)
admin.site.register(Place, PlaceAdmin)
admin.site.register(CategoryLanguage, CategoryLanguageAdmin)
admin.site.register(PlaceLanguage, PlaceLanguageAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Images)
admin.site.register(wishist, wishistAdmin)
#</editor-fold>