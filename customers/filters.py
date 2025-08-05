from dj_rql.filter_cls import AutoRQLFilterClass

from .models import Customer


class CustomerFilterClass(AutoRQLFilterClass):
    MODEL = Customer
