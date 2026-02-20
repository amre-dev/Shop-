from django.contrib import admin
from .models import Category, Product, ProductImage, Order, OrderItem

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'position')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('position',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'quantity', 'is_visible')
    list_filter = ('category', 'is_visible')
    search_fields = ('name', 'sku')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product_name','quantity','unit_price','subtotal')
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number','customer_name','customer_phone','total_amount','status','created_at')
    list_filter = ('status','created_at')
    inlines = [OrderItemInline]
    readonly_fields = ('order_number','customer_name','customer_phone','customer_address','total_amount','status','via','note','created_at')
