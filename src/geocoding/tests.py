from django.test import TestCase
from django.core.management.base import CommandError
from django.core.management import call_command
from django.contrib.gis.geos import GEOSGeometry
from io import StringIO
import os

from geoinsee.management.commands.load_township import Command
from geoinsee.models import AdministrativeEntity, ZIPCode

class LoadTownshipTest(TestCase):
    def setUp(self):
        self.cmd = Command()
        self.filename = os.path.join(os.path.dirname(__file__),
                                     'data', 'township.shp')
        self.filename_2 = os.path.join(os.path.dirname(__file__),
                                     'data', 'township_2.shp')

    def test_command_fails_if_no_arg(self):
        self.assertRaises(CommandError, call_command, 'load_township')

    def test_command_fails_if_filename_missing(self):
        self.assertRaises(CommandError, call_command, 'load_township', 'coucou.shp')

    def test_command_shows_number_of_objects(self):
        output = StringIO()
        call_command('load_township', self.filename, verbosity=2, stdout=output)
        self.assertIn('1 township found', output.getvalue())

    def test_command_add_element_in_database(self):
        call_command('load_township', self.filename)
        self.assertEqual(ZIPCode.objects.count(), 1)

        call_command('load_township', self.filename_2)
        self.assertEqual(ZIPCode.objects.count(), 3)

        self.assertEqual(AdministrativeEntity.objects.count(), 2)
        self.assertEqual(AdministrativeEntity.objects.get(insee="63113").name, "CLERMONT-FERRAND")