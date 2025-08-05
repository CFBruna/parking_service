from dj_rql.filter_cls import AutoRQLFilterClass

from .models import Vehicle, VehicleType


class VehicleTypeFilterClass(AutoRQLFilterClass):
    MODEL = VehicleType


class VehicleFilterClass(AutoRQLFilterClass):
    MODEL = Vehicle
