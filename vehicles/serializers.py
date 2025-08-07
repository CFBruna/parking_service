from django.urls import reverse
from rest_framework import serializers

from .models import Vehicle, VehicleType


class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = "__all__"


class VehicleSerializer(serializers.ModelSerializer):
    admin_url = serializers.SerializerMethodField()

    class Meta:
        model = Vehicle
        fields = [
            "id",
            "vehicle_type",
            "license_plate",
            "brand",
            "model",
            "color",
            "owner",
            "created_at",
            "updated_at",
            "admin_url",
        ]

    def get_admin_url(self, obj):
        return reverse("admin:vehicles_vehicle_changelist")
