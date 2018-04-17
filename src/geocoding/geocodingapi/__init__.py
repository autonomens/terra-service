from abc import ABCMeta, abstractmethod

from django.conf import settings
from django.utils.module_loading import import_string

class GeocodingAPI(metaclass=ABCMeta):
    @abstractmethod
    def geocode(self):
        pass

    @abstractmethod
    def reverse_geocode(self):
        pass


class GeocodingFactory(object):

    def __new__(cls, *args, **kwargs):
        try:
            module = import_string(settings.GEOCODING_PROVIDER)(*args, **kwargs)
        except ImportError as e:
            print(e)
            raise Exception('GEOCODING_PROVIDE misconfigured or inexistant module')

        return module
