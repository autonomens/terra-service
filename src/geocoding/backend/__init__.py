from abc import ABCMeta, abstractmethod

from django.conf import settings
from django.utils.module_loading import import_string

class GeocodingBackend(metaclass=ABCMeta):
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
            raise Exception('GEOCODING_PROVIDER misconfigured or inexistant module')

        return module
