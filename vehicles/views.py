from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import DjangoModelPermissions, IsAdminUser
from rest_framework.response import Response

from parking_service.permissions import IsOwnerOfVehicleOrRecord

from .filters import VehicleFilterClass, VehicleTypeFilterClass
from .models import Vehicle, VehicleType
from .serializers import VehicleSerializer, VehicleTypeSerializer
from .services import get_or_create_vehicle_with_details


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
        owner_id = request.data.get("owner")
        vehicle_type_id = request.data.get("vehicle_type")

        try:
            vehicle = get_or_create_vehicle_with_details(
                license_plate=license_plate,
                owner_id=owner_id,
                vehicle_type_id=vehicle_type_id,
            )
            serializer = self.get_serializer(vehicle)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(
                {
                    "error": "O cliente ou tipo de veículo especificado não foi encontrado."
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception:
            return Response(
                {"error": "Ocorreu um erro interno ao processar a solicitação."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
