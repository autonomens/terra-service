import logging 

from django.urls import reverse
from geoinsee.models import AdministrativeEntity

logger = logging.getLogger(__name__)

def test_state_returned_fields(client, db):
    """ Test State views returned fields  """
    response = client.get(reverse('state-list', ),)

    assert response.status_code == 200
    assert list(response.data.keys()) == ['links', 'count', 'results']
    assert (list(response.data.get('results', [{}])[0].keys()) ==
            ['name', 'insee', 'url'])

    """
    Test State with geom
    """
    response = client.get("{}?with_geom".format(reverse('state-list', ),))
    assert response.status_code == 200
    assert (list(response.data.get('results', [{}])[0].keys()) ==
            ['name', 'insee', 'url', 'geom'])

    state_code = response.data.get('results', [{}])[0].get('insee', None)

    """
    Test state detail view keys
    """
    response = client.get(reverse('state-detail', args=[state_code]))

    assert response.status_code == 200
    assert list(response.data.keys()) == ['insee', 'name']

    """
    Test counties list of a state result
    """
    response = client.get(reverse('state-counties',
                                  args=[state_code]))

    assert response.status_code == 200
    assert list(response.data.keys()) == ['links', 'count', 'results']
    assert (list(response.data.get('results', [{}])[0].keys()) ==
            ['name', 'insee', 'url'])


def test_county_returned_fields(client, db):
    """ Test County views returned fields  """
    response = client.get(reverse('county-list', ),)

    assert response.status_code == 200
    assert list(response.data.keys()) == ['links', 'count', 'results']
    assert (list(response.data.get('results', [{}])[0].keys()) ==
            ['name', 'insee', 'url'])

    """
    Test County with geom
    """
    response = client.get("{}?with_geom".format(reverse('county-list', ),))
    assert response.status_code == 200
    assert (list(response.data.get('results', [{}])[0].keys()) ==
            ['name', 'insee', 'url', 'geom'])

    state_code = response.data.get('results', [{}])[0].get('insee', None)

    # """
    # Test county detail view keys
    # """
    response = client.get(reverse('county-detail', args=[state_code]))

    assert response.status_code == 200
    assert list(response.data.keys()) == ['insee', 'name']

    # """
    # Test county list of a state result
    # """
    response = client.get(reverse('county-townships',
                                  args=[state_code]))

    assert response.status_code == 200
    assert list(response.data.keys()) == ['links', 'count', 'results']
    assert (list(response.data.get('results', [{}])[0].keys()) ==
            ['name', 'insee', 'url'])


def test_township_returned_fields(client, db):
    """ Test Township views returned fields  """
    response = client.get(reverse('township-list', ),)

    assert response.status_code == 200
    assert list(response.data.keys()) == ['links', 'count', 'results']
    assert (list(response.data.get('results', [{}])[0].keys()) ==
            ['name', 'insee', 'url'])

    """
    Test Township with geom
    """
    response = client.get("{}?with_geom".format(reverse('township-list', ),))
    assert response.status_code == 200
    assert (list(response.data.get('results', [{}])[0].keys()) ==
            ['name', 'insee', 'url', 'geom'])

    state_code = response.data.get('results', [{}])[0].get('insee', None)

    """
    Test township detail view keys
    """
    response = client.get(reverse('township-detail',
                                  args=[state_code]))

    assert response.status_code == 200
    assert list(response.data.keys()) == ['insee', 'name']

    """ Test population view """
    response = client.get(reverse('township-population', args=[state_code]))
    assert len(response.data) > 0
    assert list(response.data[0].keys()) == ['date', 'population']


def test_invalid_endpoint(client, settings):
    settings.INSEE_API_URL = 'http://my.failing.url/with/endpoint/'

    """
    Test invalid endpoint response
    """
    response = client.get(reverse('state-list'))
    assert response.status_code == 200
    assert response.data.get('count') == 0
    assert len(response.data.get('results')) == 0

    """
    Test pagination with invalid backend datas so it's and invalid
    page number
    """
    response = client.get(reverse('state-list'), {'page': 2})
    assert response.data.get('count') == 0
    assert response.data.get('links').get('next') is None
    assert response.data.get('links').get('previous') is None

def test_page_two(client):
    """
    Test links header in page 2: previous and next pages must be 
    present in this view
    """
    response = client.get(reverse('township-list'), {'page': 2})
    assert response.data.get('links').get('next') is not None
    assert response.data.get('links').get('previous') is not None

def test_entity_endpoint(client, db):
    """
    Test Entity views returned fields
    """
    entity = AdministrativeEntity(insee=10, name='Aube', geom="POINT(3.694590831032181 48.15488686123513)" )
    entity.save()
    response = client.get(reverse('entity-list', ),)

    assert response.status_code == 200
    assert (list(response.data[0].keys()) ==
            ['name', 'insee', 'url'])

    response = client.get("{}?with_geom".format(reverse('entity-list', ),))

    assert response.status_code == 200
    assert (list(response.data[0].keys()) ==
            ['name', 'insee', 'geom', 'url'])

    """
    Test state detail view keys
    """
    response = client.get(response.data[0].get('url'))

    assert response.status_code == 200
    assert list(response.data.keys()) == ['name', 'insee', 'geom', 'url']
