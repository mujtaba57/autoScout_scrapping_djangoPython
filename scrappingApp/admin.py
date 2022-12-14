from django.contrib import admin
from .models import CarDetail, CarDataIndex, DataScrapTime, CarLink, LinksIndex, LinkScrapTime

@admin.register(CarDetail)
class CarDataIndexAdmin(admin.ModelAdmin):
    list_display = (
        "carModel",
        "carMileage",
        "carRegistration",
        "carPrice"
    )
@admin.register(CarDataIndex)
class CarDataIndexAdmin(admin.ModelAdmin):
    readonly_fields = ("nameIndex",)
    list_display = (
        "nameIndex",
        "queryIndex",
        "modify_time"
    )
    def has_add_permission(self, request, object=None):
        return False

    def has_delete_permission(self, request, object=None):
        return False

@admin.register(DataScrapTime)
class DataScrapTimeAdmin(admin.ModelAdmin):
    readonly_fields = ("nameIndex",)
    list_display = (
        "startTime",
        "endTime"
    )
    def has_add_permission(self, request, object=None):
        return False
    def has_delete_permission(self, request, object=None):
        return False

@admin.register(CarLink)
class CarLinkAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "carlinks"
    )


@admin.register(LinksIndex)
class LinksIndexAdmin(admin.ModelAdmin):
    readonly_fields = ("nameIndex",)
    list_display = (
        "nameIndex",
        "yearQueryIndex",
        "priceQueryIndex",
        "carNameQueryIndex",
        "modify_time"
    )
    def has_add_permission(self, request, object=None):
        return False

    def has_delete_permission(self, request, object=None):
        return False

@admin.register(LinkScrapTime)
class LinkScrapTimeAdmin(admin.ModelAdmin):
    readonly_fields = ("nameIndex",)
    list_display = (
        "startTime",
        "endTime"
    )

    def has_add_permission(self, request, object=None):
        return False
    def has_delete_permission(self, request, object=None):
        return False

@admin.register(CarLink)
class CarLinkAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "carlinks"
    )

@admin.register(LinksIndex)
class LinksIndexAdmin(admin.ModelAdmin):
    readonly_fields = ("nameIndex",)
    list_display = (
        "nameIndex",
        "yearQueryIndex",
        "priceQueryIndex",
        "carNameQueryIndex",
        "modify_time"
    )
    # def has_add_permission(self, request, object=None):
    #     return False

    def has_delete_permission(self, request, object=None):
        return False

@admin.register(LinkScrapTime)
class LinkScrapTimeAdmin(admin.ModelAdmin):
    readonly_fields = ("nameIndex",)
    list_display = (
        "startTime",
        "endTime"
    )

    def has_add_permission(self, request, object=None):
        return False
    def has_delete_permission(self, request, object=None):
        return False