from django.contrib import admin
from menu.models import Category, FoodItem

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'vendor', 'category_description', 'created_at', 'updated_at']
    list_display_links = ['vendor', 'category_name']
    prepopulated_fields = {'slug': ('category_name',)}
    search_fields = ['category_name', 'vendor__vendor_name']

class FoodItemAdmin(admin.ModelAdmin):
    list_display = ['food_title', 'category', 'vendor', 'price', 'description', 'is_available', 'created_at']
    prepopulated_fields = {'slug': ('food_title',)}
    search_fields = ['food_title', 'vendor__vendor_name', 'category__category_name']
    list_filter = ['is_available']

admin.site.register(Category, CategoryAdmin)
admin.site.register(FoodItem, FoodItemAdmin)