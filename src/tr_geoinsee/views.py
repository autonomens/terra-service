# coding: utf8
from rest_framework.decorators import detail_route
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from SPARQLWrapper import SPARQLWrapper, JSON

from django.conf import settings
from django.utils.functional import cached_property
from django.core.paginator import Paginator

from .serializers import StateSerializer, SparQLSerializer

class SparQLViewSet(viewsets.ViewSet):

    def get_detail_query(self, pk=None):
        raise NotImplementedError("Please Implement this method")

    def get_list_query(self):
        raise NotImplementedError("Please Implement this method")

    def sparql_query(self, query, many=False):
        sparql = SPARQLWrapper(settings.INSEE_SPARQL)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        raw_result = sparql.query()
        results = raw_result.convert()

        fields = self.get_query_fields(results)

        if many:
            resultlist = {}
            for item in results.get('results', {}).get('bindings', {}):
                resultitem = resultlist.setdefault(item.get('identifier').get('value'), dict())
                resultitem.update(self.get_fields_values(fields, item))
            
            serializer = SparQLSerializer(list(resultlist.values()), many=True)
            return serializer.data

        result = {}
        for item in results.get('results', {}).get('bindings', {}):
            result.update(self.get_single_item_values(item))

        serializer = SparQLSerializer(result)
        
        return serializer.data
    
    def get_query_fields(self, query):
        fields = query.get('head', {}).get('vars', [])
        if 'identifier' in fields:
            fields.remove('identifier')
        return fields
    
    def get_single_item_values(self, item):
        prop =  item.get('prop').get('value')
        return { prop[prop.rfind('#') + 1:]: item.get('value').get('value') }


    def get_fields_values(self, fields, item):
        return { field: item.get(field).get('value') for field in fields }

    def list(self, request):
        return Response(self.sparql_query(self.get_list_query(), True))

    def retrieve(self, request, pk=None):
        return Response(self.sparql_query(self.get_detail_query(pk)))


class StateViewSet(SparQLViewSet):

    def get_detail_query(self, pk=None):
        query = '''
            PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfschema:<http://www.w3.org/2000/01/rdf-schema#>
            PREFIX igeo:<http://rdf.insee.fr/def/geo#>
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
            PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX igeo:<http://rdf.insee.fr/def/geo#>
            SELECT ?identifier ?name ?insee_code WHERE {
                    ?identifier rdf:type igeo:Region .
                    ?identifier igeo:nom ?name .
                    ?identifier igeo:vivant true .
                    ?identifier igeo:codeINSEE ?insee_code .
            }
            '''
        
    def get_counties_query(self, pk):
        query = '''
            PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX igeo:<http://rdf.insee.fr/def/geo#>
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
        return Response(self.sparql_query(self.get_counties_query(pk), True))


class CountyViewSet(SparQLViewSet):
    def get_detail_query(self, pk=None):
        query = '''
            PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfschema:<http://www.w3.org/2000/01/rdf-schema#>
            PREFIX igeo:<http://rdf.insee.fr/def/geo#>
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
            PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX igeo:<http://rdf.insee.fr/def/geo#>
            SELECT ?identifier ?name ?insee_code WHERE {
                    ?identifier rdf:type igeo:Departement .
                    ?identifier igeo:nom ?name .
                    ?identifier igeo:vivant true .
                    ?identifier igeo:codeINSEE ?insee_code .
            }
            '''

    def get_townships_query(self, pk):
        query = '''
            PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX igeo:<http://rdf.insee.fr/def/geo#>
            SELECT ?identifier ?name ?insee_code WHERE {{
                    ?identifier <http://rdf.insee.fr/def/geo#subdivisionDe> ?county .
                    ?identifier <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://rdf.insee.fr/def/geo#Commune> .
                    ?identifier <http://rdf.insee.fr/def/geo#nom> ?name .
                    ?identifier <http://rdf.insee.fr/def/geo#codeINSEE> ?insee_code .
                    ?state igeo:codeINSEE ?county_insee_code
                    FILTER( "{}" = STR(?county_insee_code))
            }}
        '''
        return query.format(pk)
        
    @detail_route(url_path='townships')
    def townships(self, request, pk):
        return Response(self.sparql_query(self.get_townships_query(pk), True))


class TownshipViewset(SparQLViewSet):
    def get_list_query(self):
        return '''
            PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX igeo:<http://rdf.insee.fr/def/geo#>
            SELECT ?identifier ?name ?insee_code WHERE {
                    ?identifier rdf:type igeo:Commune .
                    ?identifier igeo:nom ?name .
                    ?identifier igeo:vivant true .
                    ?identifier igeo:codeINSEE ?insee_code .
            }
        '''