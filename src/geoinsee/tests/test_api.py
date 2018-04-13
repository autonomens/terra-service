import json

from django.urls import reverse
from django.test import TestCase

from rest_framework.test import APIClient, force_authenticate

class APIFieldsTestCase(TestCase):
    def setUp(self):
        pass

    def test_state_returned_fields(self):
        """ Test State views returned fields  """
        response = self.client.get(reverse('state-list', ),)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.data.keys()), ['links', 'count', 'results'])
        self.assertEqual(list(response.data.get('results', [{}])[0].keys()),
                        ['name', 'insee', 'url'])

        state_code = response.data.get('results', [{}])[0].get('insee', None)
        
        """
        Test state detail view keys 
        """
        response = self.client.get(reverse('state-detail', args=[state_code]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.data.keys()), ['insee', 'name'])

        """
        Test counties list of a state result
        """
        response = self.client.get(reverse('state-counties', args=[state_code]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.data.keys()), ['links', 'count', 'results'])
        self.assertEqual(list(response.data.get('results', [{}])[0].keys()),
                        ['name', 'insee', 'url'])

    def test_county_returned_fields(self):
        """ Test County views returned fields  """
        response = self.client.get(reverse('county-list', ),)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.data.keys()), ['links', 'count', 'results'])
        self.assertEqual(list(response.data.get('results', [{}])[0].keys()),
                        ['name', 'insee', 'url'])

        state_code = response.data.get('results', [{}])[0].get('insee', None)
        
        """
        Test county detail view keys 
        """
        response = self.client.get(reverse('county-detail', args=[state_code]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.data.keys()), ['insee', 'name'])

        """
        Test county list of a state result
        """
        response = self.client.get(reverse('county-townships', args=[state_code]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.data.keys()), ['links', 'count', 'results'])
        self.assertEqual(list(response.data.get('results', [{}])[0].keys()),
                        ['name', 'insee', 'url'])


    def test_township_returned_fields(self):
        """ Test Township views returned fields  """
        response = self.client.get(reverse('township-list', ),)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.data.keys()), ['links', 'count', 'results'])
        self.assertEqual(list(response.data.get('results', [{}])[0].keys()),
                        ['name', 'insee', 'url'])

        state_code = response.data.get('results', [{}])[0].get('insee', None)
        
        """
        Test township detail view keys 
        """
        response = self.client.get(reverse('township-detail', args=[state_code]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.data.keys()), ['insee', 'name'])
