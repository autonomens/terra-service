import json
import os

import unittest

from django.test import SimpleTestCase
from django.utils.functional import cached_property

from geoinsee.utils import SparQLUtils


class SparQLUtilTestCase(SimpleTestCase):

    endpoint = "http://rdf.insee.fr/sparql"
    query = """
            SELECT ?prop ?value WHERE {
                    ?state rdf:type igeo:Region .
                    ?state igeo:nom ?name .
                    ?state igeo:vivant true .
                    ?state igeo:codeINSEE ?insee .
                    ?prop rdfschema:label ?label .
                    ?state ?prop ?value
                    FILTER( isLiteral(?value) )
            }
    """

    test_datas_items = {
        'head': {'vars': ['prop', 'value']},
        'results': {'bindings': [{
            'prop': {
                'type': 'uri',
                'value': 'http://rdf.insee.fr/def/geo#codeINSEE'},
            'value': {'datatype': 'http://www.w3.org/2001/XMLSchema#token',
                      'type': 'literal',
                      'value': '11'}},
            {'prop': {'type': 'uri',
                      'value': 'http://rdf.insee.fr/def/geo#codeRegion'},
             'value': {'datatype': 'http://www.w3.org/2001/XMLSchema#token',
                       'type': 'literal',
                       'value': '11'}},
            {'prop': {'type': 'uri',
                      'value': 'http://rdf.insee.fr/def/geo#nom'},
             'value': {'type': 'literal',
                       'value': 'Île-de-France',
                       'xml:lang': 'fr'}},
            {'prop': {'type': 'uri',
                      'value': 'http://rdf.insee.fr/def/geo#vivant'},
             'value': {'datatype': 'http://www.w3.org/2001/XMLSchema#boolean',
                       'type': 'literal',
                       'value': 'true'}},
            {'prop': {'type': 'uri',
                      'value': 'http://rdf.insee.fr/def/geo#nomCharniereClair'},
             'value': {'type': 'literal',
                       'value': 'Île-de-France',
                       'xml:lang': 'fr'}},
            {'prop': {'type': 'uri',
                      'value': 'http://rdf.insee.fr/def/geo#codeINSEE'},
             'value': {'datatype': 'http://www.w3.org/2001/XMLSchema#token',
                       'type': 'literal',
                       'value': '02'}},
            {'prop': {'type': 'uri',
                      'value': 'http://rdf.insee.fr/def/geo#codeRegion'},
             'value': {'datatype': 'http://www.w3.org/2001/XMLSchema#token',
                       'type': 'literal',
                       'value': '02'}},
            {'prop': {'type': 'uri',
                      'value': 'http://rdf.insee.fr/def/geo#nom'},
             'value': {'type': 'literal',
                       'value': 'Martinique',
                       'xml:lang': 'fr'}},
            {'prop': {'type': 'uri',
                      'value': 'http://rdf.insee.fr/def/geo#vivant'},
             'value': {'datatype': 'http://www.w3.org/2001/XMLSchema#boolean',
                       'type': 'literal',
                       'value': 'true'}},
            {'prop': {'type': 'uri',
                      'value': 'http://rdf.insee.fr/def/geo#nomCharniereClair'},
             'value': {'type': 'literal',
                       'value': 'Martinique',
                       'xml:lang': 'fr'}}]}}

    single_item = {
        'prop': {
            'xml:lang': 'fr',
            'type': 'literal',
            'value': 'Île-de-France'
        }
    }

    @unittest.skipIf('TEST_USE_REMOTE' not in os.environ,
                     'Do not use real queries if TEST_USE_REMOTE is not set')
    def test_sparql_query(self):
        self.assertEquals(self.sparql_data_items, self.test_datas_items)

    @cached_property
    def sparql_data_items(self):
        if 'TEST_USE_REMOTE' in os.environ:
            return SparQLUtils.sparql_query(self.query, 10, 0)
        else:
            return self.test_datas_items

    def get_single_item(self):
        return self.sparql_data_items.get('results').get('bindings')[0]

    def test_get_query_fields(self):
        qf = SparQLUtils.get_query_fields(self.sparql_data_items)
        self.assertEqual(['prop','value'], qf)

    def test_get_single_item_values(self):
        single_item = self.get_single_item()
        qf = SparQLUtils.get_single_item_values(single_item)
        self.assertEqual(
            list(qf.keys()),
            [single_item.get('prop').get('value').split('#')[1], ])
        self.assertEqual(
            list(qf.values()),
            [single_item.get('value').get('value'), ]
        )

    def test_get_fields_values(self):
        
        fields = SparQLUtils.get_query_fields(self.sparql_data_items)
        item = self.get_single_item()

        values = SparQLUtils.get_fields_values(fields, item)
        self.assertEqual(list(values.keys()), ['prop', 'value'])
