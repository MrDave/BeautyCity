from django.contrib import admin
from beauty_city_app.models import Shop, Client, Service, Specialist, TimeSlot, Appointment, Review


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    pass

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    raw_id_fields = ["services"]


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    pass


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    pass

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass