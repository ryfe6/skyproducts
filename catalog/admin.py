from django.contrib import admin

from catalog.models import Category, Product, BlogWrite


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category',)
    list_filter = ('category',)
    search_fields = ('name', 'description',)



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'pk',)


@admin.register(BlogWrite)
class BlogWriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'heading',)