from django.contrib import admin
from .models import ParkingRecord, ParkingSpot


@admin.register(ParkingSpot)
class ParkingSpotAdmin(admin.ModelAdmin):
    list_display = ['spot_number', 'is_occupied', 'created_at']
    search_fields = ['spot_number']
    list_filter = ['is_occupied']


class ExitStatusFilter(admin.SimpleListFilter):
    title = 'Saída registrada'
    parameter_name = 'exit_time'

    def lookups(self, request, model_admin):
        return [('no', 'Sem saída'), ('yes', 'Com saída')]
    
    def queryset(self, request, queryset):
        if self.value() == 'no':
            return queryset.filter(exit_time__isnull=True)
        if self.value() == 'yes':
            return queryset.filter(exit_time__isnull=False)


@admin.register(ParkingRecord)
class ParkingRecordAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'parking_spot', 'entry_time', 'exit_time']
    search_fields = ['vehicle__license_plate', 'parking_spot__spot_number']
    list_filter = [ExitStatusFilter]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'parking_spot' and not request.resolver_match.url_name.endswith('change'):
            kwargs['queryset'] = ParkingSpot.objects.filter(is_occupied=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
