from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .serializers import StateSerializer, SparQLSerializer
from .utils import SparQLUtils, PaginationMixin


class SparQLViewSet(viewsets.ViewSet, PaginationMixin):
    def get_detail_query(self, pk=None):
        raise NotImplementedError("Please Implement this method")

    def get_list_query(self):
        raise NotImplementedError("Please Implement this method")

    def get_item_url(self, identifier):
        raise NotImplementedError("Please Implement this method")

    def update_items_url(self, items, url_name):
        if isinstance(items, list) and url_name:
            for item in items:
                item.update({
                    'url': reverse(url_name, args=[item.get('insee_code'), ], request=self.request)
                })

    def sparql_query(self, query, page=1, many=False, item_url_name=None):
        results = SparQLUtils.sparql_query(query, self.page_size, self.page_size * (page - 1))

        fields = SparQLUtils.get_query_fields(results)

        if many:
            resultlist = {}
            for item in results.get('results', {}).get('bindings', {}):
                resultitem = resultlist.setdefault(item.get('identifier').get('value'), dict())
                resultitem.update(SparQLUtils.get_fields_values(fields, item))
            resultlist = list(resultlist.values())

            self.update_items_url(resultlist, item_url_name)
            serializer = SparQLSerializer(resultlist, many=True)

            return {
                'links': {
                    'next': self.get_next_page(page),
                    'previous': self.get_prev_page(page),
                },
                'count': self.count,
                'results': serializer.data,
            }

        result = {}
        for item in results.get('results', {}).get('bindings', {}):
            result.update(SparQLUtils.get_single_item_values(item))

        serializer = SparQLSerializer(result)
        return serializer.data
    
    def list(self, request):
        return Response(self.sparql_query(
            self.get_list_query(),
            self.get_page(request),
            True,
            '{}-detail'.format(self.basename)
            ))

    def retrieve(self, request, pk=None):
        return Response(self.sparql_query(self.get_detail_query(pk), self.get_page(request)))

    @detail_route(url_path='population')
    def population_by_date(self, request, pk):
        query = '''
            SELECT ?date ?population WHERE {{
                    ?township igeo:codeINSEE ?insee_code .
                    ?township demo:population ?demo .
                    ?demo demo:date ?date .
                    ?demo demo:populationTotale ?population .
                    FILTER( "{}" = STR(?insee_code)) .
            }} ORDER BY DESC(?date)
        '''
        results = SparQLUtils.sparql_query(query.format(pk))
        fields = SparQLUtils.get_query_fields(results)
        return Response([SparQLUtils.get_fields_values(fields, item) 
                for item in results.get('results', {}).get('bindings', {})])


class StateViewSet(SparQLViewSet):

    def get_detail_query(self, pk=None):
        query = '''
            SELECT ?prop ?value WHERE {{
                    ?state rdf:type igeo:Region .
                    ?state igeo:nom ?name .
                    ?state igeo:vivant true .
                    ?state igeo:codeINSEE ?insee_code .
                    ?prop rdfschema:label ?label .
                    ?state ?prop ?value
                    FILTER( "{}" = STR(?insee_code)) .
                    FILTER( isLiteral(?value) )
            }}
            '''
        return query.format(pk)

    def get_list_query(self):
        return '''
            SELECT ?identifier ?name ?insee_code WHERE {
                    ?identifier rdf:type igeo:Region .
                    ?identifier igeo:nom ?name .
                    ?identifier igeo:vivant true .
                    ?identifier igeo:codeINSEE ?insee_code .
            }
            '''
        
    def get_counties_query(self, pk):
        query = '''
            SELECT ?identifier ?name ?insee_code WHERE {{
                    ?identifier <http://rdf.insee.fr/def/geo#subdivisionDe> ?state .
                    ?identifier <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://rdf.insee.fr/def/geo#Departement> .
                    ?identifier <http://rdf.insee.fr/def/geo#nom> ?name .
                    ?identifier <http://rdf.insee.fr/def/geo#codeINSEE> ?insee_code .
                    ?state igeo:codeINSEE ?state_insee_code
                    FILTER( "{}" = STR(?state_insee_code))
            }}
        '''
        return query.format(pk)

    @detail_route(url_path='counties')
    def counties(self, request, pk):
        return Response(self.sparql_query(
            self.get_counties_query(pk),
            self.get_page(request),
            True,
            'county-detail'))

    def get_item_url(self, identifier):
        return reverse('county-detail', args=[identifier, ])

class CountyViewSet(SparQLViewSet):
    def get_detail_query(self, pk=None):
        query = '''
            SELECT ?prop ?value WHERE {{
                    ?county rdf:type igeo:Departement .
                    ?county igeo:nom ?name .
                    ?county igeo:vivant true .
                    ?county igeo:codeINSEE ?insee_code .
                    ?prop rdfschema:label ?label .
                    ?county ?prop ?value
                    FILTER( "{}" = STR(?insee_code)) .
                    FILTER( isLiteral(?value) )
            }}
            '''
        return query.format(pk)

    def get_list_query(self):
        return '''
            SELECT ?identifier ?name ?insee_code WHERE {
                    ?identifier rdf:type igeo:Departement .
                    ?identifier igeo:nom ?name .
                    ?identifier igeo:vivant true .
                    ?identifier igeo:codeINSEE ?insee_code .
            }
            '''

    def get_townships_query(self, pk):
        query = '''
            SELECT ?identifier ?name ?insee_code WHERE {{
                    ?identifier igeo:subdivisionDe ?county .
                    ?identifier rdf:type igeo:Commune .
                    ?identifier igeo:nom ?name .
                    ?identifier igeo:codeINSEE ?insee_code .
                    ?county igeo:codeINSEE ?county_insee_code
                    FILTER( "{}" = STR(?county_insee_code))
            }}
        '''
        return query.format(pk)

    @detail_route(url_path='townships')
    def townships(self, request, pk):
        return Response(self.sparql_query(
            self.get_townships_query(pk),
            self.get_page(request),
            True,
            'township-detail'))


class TownshipViewset(SparQLViewSet):
    def get_detail_query(self, pk=None):
        query = '''
            SELECT ?prop ?value WHERE {{
                    ?township rdf:type igeo:Commune .
                    ?township igeo:nom ?name .
                    ?township igeo:vivant true .
                    ?township igeo:codeINSEE ?insee_code .
                    ?prop rdfschema:label ?label .
                    ?township ?prop ?value
                    FILTER( "{}" = STR(?insee_code)) .
                    FILTER( isLiteral(?value) )
            }}
            '''
        return query.format(pk)


    def get_list_query(self):
        return '''
            SELECT ?identifier ?name ?insee_code WHERE {
                    ?identifier rdf:type igeo:Commune .
                    ?identifier igeo:nom ?name .
                    ?identifier igeo:vivant true .
                    ?identifier igeo:codeINSEE ?insee_code .
            }
        '''
