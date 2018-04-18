import os
import pytest

from geoinsee.utils import SparQLUtils

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
                  'value':
                  'http://rdf.insee.fr/def/geo#nomCharniereClair'},
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
                  'value':
                  'http://rdf.insee.fr/def/geo#nomCharniereClair'},
            'value': {'type': 'literal',
                      'value': 'Martinique',
                      'xml:lang': 'fr'}}]}}


@pytest.fixture(scope="module")
def sparql_single_item(sparql_data_items):
    return sparql_data_items.get('results').get('bindings')[0]


@pytest.fixture(scope="module")
def sparql_data_items():
    if 'TEST_USE_REMOTE' in os.environ:
        return SparQLUtils.sparql_query(query, 10, 0)
    else:
        return test_datas_items


@pytest.mark.skipIf('TEST_USE_REMOTE' not in os.environ,
                    reason=('Do not use real queries if '
                            'TEST_USE_REMOTE is not set'))
def test_sparql_query(sparql_data_items):
    assert sparql_data_items == test_datas_items


def test_get_query_fields(sparql_data_items):
    qf = SparQLUtils.get_query_fields(sparql_data_items)
    assert qf == ['prop', 'value']


def test_get_single_item_values(sparql_single_item):
    qf = SparQLUtils.get_single_item_values(sparql_single_item)
    assert list(qf.keys()) == [(sparql_single_item.get('prop')
                                .get('value').split('#')[1]), ]
    assert list(qf.values()) == [(sparql_single_item.get('value')
                                  .get('value')), ]


def test_get_fields_values(sparql_data_items, sparql_single_item):
    fields = SparQLUtils.get_query_fields(sparql_data_items)
    item = sparql_single_item

    values = SparQLUtils.get_fields_values(fields, item)
    assert list(values.keys()) == ['prop', 'value']
