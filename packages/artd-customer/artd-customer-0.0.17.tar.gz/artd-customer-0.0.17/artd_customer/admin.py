from django.contrib import admin
from artd_customer.models import (
    Customer,
    Tag,
    CustomerTag,
    CustomerAddress,
    CustomerAdditionalFields,
    CustomerGroup,
    CustomerGroupChangeLog,
)
from django_json_widget.widgets import JSONEditorWidget
from django.db import models


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    search_fields = [
        "name",
        "phone",
        "email",
        "partner__name",
    ]
    list_display = [
        "id",
        "name",
        "phone",
        "email",
        "status",
    ]

    def has_delete_permission(self, request, obj=None):
        return False

    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = [
        "description",
    ]
    list_display = [
        "description",
    ]


@admin.register(CustomerTag)
class CustomerTagAdmin(admin.ModelAdmin):
    search_fields = [
        "customer",
        "tag",
    ]
    list_display = [
        "customer",
        "tag",
    ]


@admin.register(CustomerAddress)
class CustomerAddressAdmin(admin.ModelAdmin):
    search_fields = [
        "customer__email",
        "city__name",
        "phone",
        "address",
    ]
    list_display = [
        "customer",
        "city",
        "phone",
        "address",
    ]
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }


@admin.register(CustomerAdditionalFields)
class CustomerAdditionalFieldsAdmin(admin.ModelAdmin):
    search_fields = [
        "partner__name",
        "name",
        "field_type",
        "label",
        "required",
    ]
    list_display = [
        "partner",
        "name",
        "field_type",
        "label",
        "required",
    ]

@admin.register(CustomerGroup)
class CustomerGroupAdmin(admin.ModelAdmin):
    search_fields = [
        "group_code",
        "group_name",
        "status",
        "created_at",
        "updated_at",
    ]
    list_display = [
        "group_code",
        "group_name",
        "status",
        "created_at",
        "updated_at",
    ]
    readonly_fields = [
        "created_at",
        "updated_at",
    ]

@admin.register(CustomerGroupChangeLog)
class CustomerGroupChangeLogAdmin(admin.ModelAdmin):
    search_fields = [
        "customer",
        "old_group",
        "new_group",
    ]
    list_display = [
        "customer",
        "old_group",
        "new_group",
        "status",
        "created_at",
        "updated_at",
    ]
    readonly_fields = [
        "customer",
        "old_group",
        "new_group",
        "status",
        "created_at",
        "updated_at",
    ]