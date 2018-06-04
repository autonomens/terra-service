import argparse
import logging
import os

from django.contrib.gis.gdal import DataSource
from django.core.management.base import BaseCommand, CommandError
from geoinsee.models import AdministrativeEntity, ZIPCode

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Load administrative entities from shapefiles in database"

    def add_arguments(self, parser):
        parser.add_argument('shapefile', type=argparse.FileType('rb'))
        parser.add_argument('--encoding', default='utf-8',
                            help='Specify encoding (utf-8 by default)')
        parser.add_argument(
            '--area-type', help='Specify administrative area type', required=False)

    def handle(self, *args, **options):
        shapefile = options.get('shapefile')
        encoding = options.get('encoding')
        entity_type = options.get('area_type')
        datasource = DataSource(shapefile.name, encoding=encoding)
        count = datasource.layer_count
        logger.info('%s layers found' % count)
        geometry, name, insee_code = ([] for i in range(3))

        for layer in datasource:
            geometry.extend(layer.get_geoms(geos=True))
            name.extend(layer.get_fields('nom'))
            insee_code.extend(layer.get_fields('code_insee'))

        logger.info('%s states found' % len(geometry))

        for i, geom in enumerate(geometry):
            entity, _ = AdministrativeEntity.objects.update_or_create(
                insee=insee_code[i],
                entity_type=entity_type,
                defaults={'geom': geom, 'name': name[i]}
            )
        self.stdout.write('DONE')
