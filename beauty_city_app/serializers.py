from rest_framework import serializers

from beauty_city_app.models import Appointment, TimeSlot


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ["specialist", "date", "time", "shop"]


class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = ["id", "client", "service", "price", "time_slot", "is_paid"]
