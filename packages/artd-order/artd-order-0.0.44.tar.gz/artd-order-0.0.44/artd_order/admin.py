from django.contrib import admin
from artd_order.models import (
    OrderStatus,
    Order,
    OrderProduct,
    OrderStatusHistory,
    OrderPaymentHistory,
    OrderDeliveryMethod,
    OrderAdress,
)
from django_json_widget.widgets import JSONEditorWidget
from django.db import models


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "status_code",
        "status_description",
    )
    list_display_links = (
        "id",
        "status_code",
        "status_description",
    )
    search_fields = (
        "id",
        "status_code",
        "status_description",
    )
    list_filter = (
        "status_code",
        "status_description",
    )
    list_per_page = 25
    ordering = ("status_description",)
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )


@admin.register(OrderDeliveryMethod)
class OrderDeliveryMethodAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "delivery_method_code",
    )
    search_fields = (
        "id",
        "delivery_method_code",
    )
    list_filter = ("delivery_method_code",)
    list_per_page = 25
    ordering = ("order",)
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "increment_id",
        "partner",
        "customer",
        "order_status",
        "created_at",
        "payment_code",
        "grand_total",
        "status",
    )
    search_fields = (
        "id",
        "payment_code",
        "partner__name",
        "order_status__status_code",
        "created_at",
        "increment_id",
        "customer__email",
    )
    list_filter = (
        "partner",
        "payment_code",
        "order_status",
        "created_at",
        "grand_total",
    )
    list_per_page = 25
    ordering = ("created_at",)
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "product",
        "quantity",
        "base_amount",
        "total",
    )
    search_fields = (
        "id",
        "order__increment_id",
        "product__name",
        "quantity",
        "base_amount",
        "total",
    )
    list_filter = (
        "order",
        "product",
        "quantity",
        "base_amount",
        "total",
    )
    list_per_page = 25
    ordering = ("order",)
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }


@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "order_status",
        "comment",
    )
    search_fields = (
        "id",
        "order__increment_id",
        "order_status__status_code",
        "comment",
    )
    list_filter = (
        "order",
        "order_status",
        "comment",
    )
    list_per_page = 25
    ordering = ("order",)
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }


@admin.register(OrderPaymentHistory)
class OrderPaymentHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "payment_code",
    )
    search_fields = (
        "id",
        "order__increment_id",
        "payment_code",
    )
    list_filter = (
        "order",
        "payment_code",
        "created_at",
    )
    list_per_page = 25
    ordering = ("order",)
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }


@admin.register(OrderAdress)
class OrderAdressAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "address_type",
        "city",
        "address",
        "phone",
    )
    search_fields = (
        "id",
        "order__increment_id",
        "address_type",
        "city",
        "address",
        "phone",
    )
    list_filter = (
        "order",
        "address_type",
        "city",
        "address",
        "phone",
    )
    list_per_page = 25
    ordering = ("order",)
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
