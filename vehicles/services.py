from faker import Faker
from faker_vehicle import VehicleProvider

from customers.models import Customer

from .models import Vehicle, VehicleType


def get_or_create_vehicle_with_details(
    license_plate: str, owner_id: int = None, vehicle_type_id: int = None
) -> Vehicle:
    if not license_plate:
        raise ValueError("A placa do veículo é obrigatória.")

    defaults = {}
    if owner_id:
        defaults["owner"] = Customer.objects.get(pk=owner_id)
    if vehicle_type_id:
        defaults["vehicle_type"] = VehicleType.objects.get(pk=vehicle_type_id)

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
    else:
        updated = False
        if owner_id and vehicle.owner_id != owner_id:
            vehicle.owner_id = owner_id
            updated = True
        if vehicle_type_id and vehicle.vehicle_type_id != vehicle_type_id:
            vehicle.vehicle_type_id = vehicle_type_id
            updated = True
        if updated:
            vehicle.save(update_fields=["owner", "vehicle_type", "updated_at"])

    return vehicle
