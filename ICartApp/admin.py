from django.contrib import admin
from .models import *
# Register your models here.

class ImagesTabularInline(admin.TabularInline):
    model=Images

class ProductAdmin(admin.ModelAdmin):
    inlines=[ImagesTabularInline]

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(FilterPrice)
admin.site.register(Color)
admin.site.register(Product, ProductAdmin)
admin.site.register(Images)