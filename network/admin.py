from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Provider, Product, Contact


class ProductInline(admin.TabularInline):
    model = Provider.products.through
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'model', 'date_release')
    list_filter = ('title',)
    search_fields = ('title', 'model')


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'type', 'level', 'contact_country', 'contact_city', 'debt', 'supplier_link')
    list_per_page = 10

    list_filter = ('contact__city',)
    fieldsets = [
        (None, {'fields': ['title', 'type', 'level', 'products', 'supplier', 'debt', 'created_at', 'updated_at']}),
        ('Contacts', {'fields': ['contact']}),
    ]
    readonly_fields = ('level', 'created_at', 'updated_at')
    actions = ['cancel_debt', ]
    inlines = [ProductInline]

    def contact_country(self, obj):
        return obj.contact.country

    contact_country.short_description = 'Country'

    def contact_city(self, obj):
        return obj.contact.city

    contact_city.short_description = 'City'

    def supplier_link(self, obj):
        if obj.supplier:
            link = reverse('admin:network_provider_change', args=[obj.supplier.id])
            return mark_safe(f'<a href="{link}">{obj.supplier}</a>')

    supplier_link.short_description = 'Supplier'

    @admin.action(description="Cancel debt")
    def cancel_debt(self, request, queryset):
        queryset.update(debt=0)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'country', 'city', 'street', 'house')  # вы можете выбрать, какие поля отображать
    search_fields = ('email', 'country', 'city')  # и какие поля использовать для поиска
