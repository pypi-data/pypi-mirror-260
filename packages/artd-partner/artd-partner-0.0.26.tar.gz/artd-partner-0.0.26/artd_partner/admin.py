from django.contrib import admin

# Register your models here.
from django.contrib import admin
from artd_partner.models import Partner, Headquarter, Position, Coworker


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    """Admin view for Partner."""

    list_display = (
        "name",
        "partner_slug",
        "dni",
        "address",
        "city",
    )
    list_filter = (
        "city",
        "partner_slug",
    )
    search_fields = (
        "name",
        "partner_slug",
        "dni",
        "address",
        "city__name",
    )


@admin.register(Headquarter)
class HeadquarterAdmin(admin.ModelAdmin):
    """Admin view for Headquarter."""

    list_display = (
        "name",
        "address",
        "city",
        "phone",
        "partner",
    )
    list_filter = ("city", "partner")
    search_fields = (
        "name",
        "address",
        "city__name",
        "phone",
        "partner__name",
    )


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    """Admin view for Position."""

    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Coworker)
class CoworkerAdmin(admin.ModelAdmin):
    """Admin view for Coworker."""

    list_display = (
        "first_name",
        "last_name",
        "dni",
        "phone",
        "position",
        "headquarter",
    )
    list_filter = ("position", "headquarter")
    search_fields = (
        "first_name",
        "last_name",
        "dni",
        "phone",
        "position__name",
        "headquarter__name",
    )
