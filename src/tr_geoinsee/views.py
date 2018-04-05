# coding: utf8
from rest_framework.decorators import detail_route
from rest_framework import viewsets
from rest_framework.response import Response
from SPARQLWrapper import SPARQLWrapper, JSON

from django.conf import settings

from .serializers import StateSerializer

class SparQLViewSet(viewsets.ViewSet):
    
    def get_detail_query(self, pk=None):
        raise NotImplementedError("Please Implement this method")

    def get_list_query(self):
        raise NotImplementedError("Please Implement this method")

    def sparql_query(self, query):
        sparql = SPARQLWrapper(settings.INSEE_SPARQL)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        raw_result = sparql.query()
        results = raw_result.convert()

        response = []
        vars = results.get('head', {}).get('vars', [])
        for item in results.get('results', {}).get('bindings', {}):
            try:
                response.append({ var: item.get(var).get('value') for var in vars })
            except Exception:
                pass
        return response

        

    def list(self, request):
        return Response(self.sparql_query(self.get_list_query()))

    def retrieve(self, request, pk=None):
        return Response(self.sparql_query(self.get_detail_query(pk)))

class StateViewSet(SparQLViewSet):

    def get_detail_query(self, pk=None):
        query = '''
            PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX igeo:<http://rdf.insee.fr/def/geo#>
            SELECT ?label ?value WHERE {{
                    ?state rdf:type igeo:Region .
                    ?state igeo:nom ?name .
                    ?state igeo:vivant true .
                    ?state igeo:codeINSEE ?insee_code .
                    ?state ?prop ?value .
                    ?prop <http://www.w3.org/2000/01/rdf-schema#label> ?label
                    FILTER( "{}" = STR(?insee_code)) .
            }}
            '''
        return query.format(pk)

    def get_list_query(self):
        return '''
            PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX igeo:<http://rdf.insee.fr/def/geo#>
            SELECT ?name ?insee_code WHERE {
                ?state rdf:type igeo:Region .
                    ?state igeo:nom ?name .
                    ?state igeo:vivant true .
                    ?state igeo:codeINSEE ?insee_code .
            }
            '''
        
    def get_counties_query(self, pk):
        query = '''
            PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX igeo:<http://rdf.insee.fr/def/geo#>
            SELECT ?code_insee ?name WHERE {{
                    ?county_id <http://rdf.insee.fr/def/geo#subdivisionDe> ?state .
                    ?county_id <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://rdf.insee.fr/def/geo#Departement> .
                    ?county_id <http://rdf.insee.fr/def/geo#nom> ?name .
                    ?county_id <http://rdf.insee.fr/def/geo#codeINSEE> ?code_insee .
                    ?state igeo:codeINSEE ?state_insee_code
                    FILTER( "{}" = STR(?state_insee_code))
            }}
        '''
        return query.format(pk)

    @detail_route(url_path='counties')
    def counties(self, request, pk):
        return Response(self.sparql_query(self.get_counties_query(pk)))


class CountyViewSet(SparQLViewSet):
    def get_detail_query(self, pk=None):
        query = '''
            PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX igeo:<http://rdf.insee.fr/def/geo#>
            SELECT ?label ?value WHERE {{
                    ?state rdf:type igeo:Departement .
                    ?state igeo:nom ?name .
                    ?state igeo:vivant true .
                    ?state igeo:codeINSEE ?insee_code .
                    ?state ?prop ?value .
                    ?prop <http://www.w3.org/2000/01/rdf-schema#label> ?label
                    FILTER( "{}" = STR(?insee_code)) .
            }}
            '''
        return query.format(pk)

    def get_list_query(self):
        return '''
            PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX igeo:<http://rdf.insee.fr/def/geo#>
            SELECT ?name ?insee_code WHERE {
                ?state rdf:type igeo:Departement .
                    ?state igeo:nom ?name .
                    ?state igeo:vivant true .
                    ?state igeo:codeINSEE ?insee_code .
            }
            '''

    def get_townships_query(self, pk):
        query = '''
            PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX igeo:<http://rdf.insee.fr/def/geo#>
            SELECT ?code_insee ?name WHERE {{
                    ?township_id <http://rdf.insee.fr/def/geo#subdivisionDe> ?county .
                    ?township_id <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://rdf.insee.fr/def/geo#Commune> .
                    ?township_id <http://rdf.insee.fr/def/geo#nom> ?name .
                    ?township_id <http://rdf.insee.fr/def/geo#codeINSEE> ?code_insee .
                    ?county igeo:codeINSEE ?county_insee_code
                    FILTER( "{}" = STR(?county_insee_code))
            }}
        '''
        return query.format(pk)
        
    @detail_route(url_path='townships')
    def townships(self, request, pk):
        return Response(self.sparql_query(
            '''
            PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX igeo:<http://rdf.insee.fr/def/geo#>
            SELECT ?a ?b WHERE {
                <http://id.insee.fr/geo/mouvements/279> ?a ?b
            }
            ''')
        )

        return Response(self.sparql_query(self.get_townships_query(pk)))
