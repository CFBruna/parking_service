from faker import Faker
from faker_vehicle import VehicleProvider
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import DjangoModelPermissions, IsAdminUser
from rest_framework.response import Response

from parking_service.permissions import IsOwnerOfVehicleOrRecord

from .filters import VehicleFilterClass, VehicleTypeFilterClass
from .models import Vehicle, VehicleType
from .serializers import VehicleSerializer, VehicleTypeSerializer


class VehicleTypeViewSet(viewsets.ModelViewSet):
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer
    rql_filter_class = VehicleTypeFilterClass
    permission_classes = [DjangoModelPermissions, IsAdminUser]


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    rql_filter_class = VehicleFilterClass
    permission_classes = [DjangoModelPermissions, IsOwnerOfVehicleOrRecord]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Vehicle.objects.all()
        return Vehicle.objects.filter(owner__user=user)

    @action(detail=False, methods=["post"], url_path="get-by-plate")
    def get_by_plate(self, request):
        license_plate = request.data.get("license_plate")
        if not license_plate:
            return Response(
                {"error": "A placa do veículo é obrigatória."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        defaults = {}

        owner_id = request.data.get("owner")
        if owner_id:
            defaults["owner_id"] = owner_id

        vehicle_type_id = request.data.get("vehicle_type")
        if vehicle_type_id:
            defaults["vehicle_type_id"] = vehicle_type_id

        vehicle, created = Vehicle.objects.get_or_create(
            license_plate=license_plate, defaults=defaults
        )

        if created:
            if not vehicle.brand and not vehicle.model:
                fake = Faker("pt_BR")
                fake.add_provider(VehicleProvider)
                vehicle.brand = fake.vehicle_make()
                vehicle.model = fake.vehicle_model()
                vehicle.color = fake.safe_color_name()
                vehicle.save()
        elif not created:
            for key, value in defaults.items():
                setattr(vehicle, key, value)
            vehicle.save()

        serializer = self.get_serializer(vehicle)
        return Response(serializer.data, status=status.HTTP_200_OK)
