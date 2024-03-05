from django.contrib import admin
from .models import Stock, StockLog


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = (
        "partner",
        "product",
        "stock",
        "stock_min",
        "stock_max",
        "status",
    )
    list_filter = (
        "partner",
        "product",
        "stock",
        "stock_min",
        "stock_max",
        "status",
    )
    search_fields = (
        "partner__name",
        "product__name",
        "stock",
        "stock_min",
        "stock_max",
        "status",
    )
    readonly_fields = [
        "created_at",
        "updated_at",
        "status",
    ]


@admin.register(StockLog)
class StockLogAdmin(admin.ModelAdmin):
    list_display = (
        "partner",
        "product",
        "stock",
        "stock_min",
        "stock_max",
        "status",
    )
    list_filter = (
        "partner",
        "product",
        "stock",
        "stock_min",
        "stock_max",
        "status",
    )
    search_fields = (
        "partner__name",
        "product__name",
        "stock",
        "stock_min",
        "stock_max",
        "status",
    )
    readonly_fields = [
        "created_at",
        "updated_at",
        "status",
    ]
