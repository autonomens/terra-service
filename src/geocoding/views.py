from django.http import HttpResponseBadRequest 
from django.utils.functional import cached_property

from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response


from .backend import GeocodingFactory

class GeocodingViewset(viewsets.ViewSet):

    @cached_property
    def geocodingapi(self):
        return GeocodingFactory()

    @list_route(methods=['get'])
    def geocode(self, request, *args, **kwargs):
        if not 'query' in request.GET:
            return HttpResponseBadRequest() 
        return Response(self.geocodingapi.geocode(request.GET.get('query')))

    @list_route(methods=['get'])
    def reverse(self, request, *args, **kwargs):
        lat, lon = (request.GET.get('lat', None), 
                    request.GET.get('lon', None))

        if not ( lat or lon ) :
            return HttpResponseBadRequest() 

        return Response(self.geocodingapi.reverse_geocode(lat, lon))

