from django.contrib.gis.db import models
from django.conf import settings
from django.utils.translation import gettext as _
# Create your models here.


class AdministrativeEntity(models.Model):

    ENTITY_TYPE_TOWN = 'township'
    ENTITY_TYPE_SCOT = 'scot'
    ENTITY_TYPE_EPCI = 'epci'
    ENTITY_TYPE_COUNTY = 'county'
    ENTITY_TYPE_REGION = 'region'
    ENTITY_TYPE_STATE = 'state'
    ENTITY_TYPE_COUNTRY = 'country'
    ENTITY_TYPE_CHOICES = (
        (ENTITY_TYPE_TOWN, _('Township')),
        (ENTITY_TYPE_SCOT, _('SCOT')),
        (ENTITY_TYPE_EPCI, _('EPCI')),
        (ENTITY_TYPE_COUNTY, _('County')),
        (ENTITY_TYPE_REGION, _('Region')),
        (ENTITY_TYPE_STATE, _('State')), # US
        (ENTITY_TYPE_COUNTRY, _('Country')),
    )
    name = models.CharField(blank=False, max_length=163, help_text=_('Administrative Entity name'))
    insee = models.CharField(max_length=5, blank=False, help_text='Insee Code')
    entity_type = models.CharField(null=False,
        max_length=15, choices=ENTITY_TYPE_CHOICES, help_text=_('Administrative area type'))
    geom = models.GeometryField(dim=2, srid=settings.SRID, spatial_index=False, editable=False, null=False, default=None)

    class Meta:
        unique_together = ('insee', 'entity_type',)


class ZIPCode(models.Model):
    insee = models.ForeignKey(AdministrativeEntity, on_delete=models.CASCADE)
    zip_code = models.CharField(max_length=5, blank=False, unique=False, help_text='Zip Code')
