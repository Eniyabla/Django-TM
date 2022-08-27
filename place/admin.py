from django.contrib import admin

# Register your models here.
from mptt.admin import DraggableMPTTAdmin

from place.models import Category, Place


#<editor-fold desc="Category Admin">

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent', 'status']
    list_filter = ['status']
#class CategoryLanguageInline(admin.TabularInline):
   # model = CategoryLanguage
   # extra = 3
   # show_change_link = True
  #  prepopulated_fields = {'slug': ('title',)}


class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}
    #inlines = [CategoryLanguageInline,]

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
#<editor-fold desc="Place Admin">
class PlaceAdmin(admin.ModelAdmin):
    list_display = ['title', 'category','image_tag', 'status',]
    list_filter = ['category']
    readonly_fields = ['image_tag']
    #inlines = [PlaceImageInline,PlaceLanguageInline]
    prepopulated_fields = {'slug': ('title',) }
#</editor-fold >
#<editor-fold desc="Admin.site.register">
admin.site.register(Category, CategoryAdmin2)
admin.site.register(Place, PlaceAdmin)
#</editor-fold>