from django.contrib import admin
from .models import CarDetail, CarDataIndex, DetailScrapExecutionTime, AllCarLink

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
    list_display = (
        "queryIndex",
        "modify_time"
    )
    def has_add_permission(self, request, object=None):
        return False

    def has_delete_permission(self, request, object=None):
        return False

@admin.register(DetailScrapExecutionTime)
class DetailScrapExecutionTimeAdmin(admin.ModelAdmin):
    list_display = (
        "startTime",
        "endTime"
    )
    def has_delete_permission(self, request, object=None):
        return False

@admin.register(AllCarLink)
class AllCarLinkAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "link"
    )