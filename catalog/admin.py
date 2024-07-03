from django.contrib import admin
from .models import Product, Version, Category
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, Permission


class VersionInline(admin.TabularInline):
    model = Version
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'purchase_price', 'created_at', 'updated_at', 'is_published', 'owner')
    list_filter = ('category', 'is_published')
    search_fields = ('name', 'description')
    inlines = [VersionInline]

    fields = ('name', 'category', 'purchase_price', 'description', 'is_published', 'owner')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)


# Функция для создания группы и назначения прав
def create_moderator_group():
    group, created = Group.objects.get_or_create(name='Moderator')
    if created:
        content_type = ContentType.objects.get_for_model(Product)
        permissions = Permission.objects.filter(content_type=content_type, codename__in=[
            'can_unpublish_product',
            'change_description_product',
            'change_category_product'
        ])
        group.permissions.set(permissions)
        group.save()
