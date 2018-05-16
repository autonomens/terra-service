try:
    from django.contrib.gis.geoip2 import GeoIP2
except ImportError:
    GeoIP2 = None

from django.http import HttpResponseBadRequest

from rest_framework.views import APIView

from rest_framework.response import Response


class GeoIPView(APIView):
    def get(self, request, format=None):
        if not GeoIP2:
            raise Exception('GeoIP2 cannot be loaded, probably missing data files')

        if not 'ip' in request.GET or not request.GET.get('ip'):
            return HttpResponseBadRequest("Missing IP parameter")

        geoip = GeoIP2()
        return Response(geoip.city(request.GET.get('ip')))
