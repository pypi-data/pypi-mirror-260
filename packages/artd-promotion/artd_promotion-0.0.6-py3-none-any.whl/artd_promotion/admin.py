from django.contrib import admin
from artd_promotion.models import Coupon, PromotionRule

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = [
        "partner",
        "code",
        "name",
        "start_date",
        "end_date",
        "is_percentage",
        "value",
        "status",
        "created_at",
        "updated_at",
    ]
    list_filter = [
        "partner",
        "start_date",
        "end_date",
        "is_percentage",
        "status",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "code",
        "name",
    ]
    readonly_fields = [
        "created_at",
        "updated_at",
    ]

@admin.register(PromotionRule)
class PromotionRuleAdmin(admin.ModelAdmin):
    list_display = [
        "coupon",
        "status",
        "created_at",
        "updated_at",
    ]
    list_filter = [
        "status",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "coupon",
        "description",
    ]
    readonly_fields = [
        "created_at",
        "updated_at",
    ]
