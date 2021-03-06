from rest_framework import routers

from .views import StateViewSet, CountyViewSet, CantonViewSet, TownshipViewset, AdministrativeEntityViewset

router = routers.SimpleRouter()

router.register(r'state', StateViewSet, base_name='state')
router.register(r'county', CountyViewSet, base_name='county')
router.register(r'canton', CantonViewSet, base_name='canton')
router.register(r'township', TownshipViewset, base_name='township')
router.register(r'entity', AdministrativeEntityViewset, base_name='entity')


urlpatterns = []
urlpatterns += router.urls
