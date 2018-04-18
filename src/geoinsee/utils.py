import logging
from math import ceil
import numbers

from SPARQLWrapper import SPARQLWrapper, JSON

from django.conf import settings
from django.utils.functional import cached_property

from rest_framework.utils.urls import replace_query_param

logger = logging.getLogger(__name__)

class SparQLUtils(object):
    @staticmethod
    def sparql_query(query, limit=None, offset=None):
        """
        Run a SparQL query on INSEE_API_URL endpoint with pre-defined
        prefixes and limit management
        """
        sparql_query = '''
            PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfschema:<http://www.w3.org/2000/01/rdf-schema#>
            PREFIX igeo:<http://rdf.insee.fr/def/geo#>
            PREFIX demo:<http://rdf.insee.fr/def/demo#>
            {query}
        '''

        format_keywords = {
            'query': query,
        }

        if (isinstance(offset, numbers.Integral) and
            isinstance(limit, numbers.Integral)):

            sparql_query += '''
                LIMIT {limit}
                OFFSET {offset}
            '''
            format_keywords.update({
                'limit': limit,
                'offset': offset,
            })

        try:
            sparql = SPARQLWrapper(settings.INSEE_API_URL)
            sparql.setQuery(sparql_query.format(**format_keywords))
            sparql.setReturnFormat(JSON)
            raw_result = sparql.query()
            return raw_result.convert()
        except Exception as e:
            logger.critical("A fatal error occured with SparQL endpoint: {}".format(e))
            return {}

    @staticmethod
    def get_query_fields(query):
        """ Return field list of a query """
        fields = query.get('head', {}).get('vars', [])
        if 'identifier' in fields:
            fields.remove('identifier')
        return fields

    @staticmethod
    def get_single_item_values(item):
        """ return formatted content for single item query """
        prop = item.get('prop').get('value')
        return {prop[prop.rfind('#') + 1:]: item.get('value').get('value')}

    @staticmethod
    def get_fields_values(fields, item):
        """ return dict() of fields and associated values """
        return {field: item.get(field).get('value') for field in fields}


class PaginationMixin(object):
    page_size = 10
    page_query_param = 'page'

    @cached_property
    def count(self):
        """ Count of elements in a SparQL query """
        count_query = '''
            SELECT (COUNT(*) AS ?count)
            WHERE {{
                {}
            }}
        '''
        try:
            result = SparQLUtils.sparql_query(
                count_query.format(self.get_list_query())
            )

            return int(result.get('results', {}).get('bindings', {})[0]
                       .get('count', {}).get('value', 0))
        except Exception as e:
            logger.warning("Error in SparQL result: {}".format(e))
            return 0

    @cached_property
    def num_pages(self):
        """Return the total number of pages."""
        if self.count == 0:
            return 0
        hits = max(1, self.count)
        return int(ceil(hits / float(self.page_size)))

    def get_page(self, request):
        """ return the current page number """
        page = int(request.GET.get('page')) if 'page' in request.GET else 1
        return page if self.is_valid_page_number(page) else 1

    def is_valid_page_number(self, page):
        """ test if the page number is legal """
        return 0 < page <= self.num_pages

    def get_next_page(self, current_page):
        """ return next page url """
        url = self.request.build_absolute_uri()
        page_number = current_page + 1

        if self.is_valid_page_number(page_number):
            return replace_query_param(url, self.page_query_param, page_number)
        return None

    def get_prev_page(self, current_page):
        """ return previous page url """
        url = self.request.build_absolute_uri()
        page_number = current_page - 1

        if self.is_valid_page_number(page_number):
            return replace_query_param(url, self.page_query_param, page_number)
        return None
