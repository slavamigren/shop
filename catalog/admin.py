from django.contrib import admin

from catalog.models import Category, Product, Contact, ForbiddenWords, ProductVersion


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'price', 'category', 'owner')
    list_filter = ('category',)
    search_fields = ('name', 'description')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'phone_number', 'user_text')
    search_fields = ('name', 'user_text')

@admin.register(ForbiddenWords)
class ForbiddenWordsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'word')
    search_fields = ('word',)

@admin.register(ProductVersion)
class ProductVersionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'product', 'num', 'name', 'is_actual')
    search_fields = ('product',)