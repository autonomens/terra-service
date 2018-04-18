import logging 

from django.urls import reverse

logger = logging.getLogger(__name__)

def test_state_returned_fields(client):
    """ Test State views returned fields  """
    response = client.get(reverse('state-list', ),)

    assert response.status_code == 200
    assert list(response.data.keys()) == ['links', 'count', 'results']
    assert (list(response.data.get('results', [{}])[0].keys()) ==
            ['name', 'insee', 'url'])

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


def test_county_returned_fields(client):
    """ Test County views returned fields  """
    response = client.get(reverse('county-list', ),)

    assert response.status_code == 200
    assert list(response.data.keys()) == ['links', 'count', 'results']
    assert (list(response.data.get('results', [{}])[0].keys()) ==
            ['name', 'insee', 'url'])

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


def test_township_returned_fields(client):
    """ Test Township views returned fields  """
    response = client.get(reverse('township-list', ),)

    assert response.status_code == 200
    assert list(response.data.keys()) == ['links', 'count', 'results']
    assert (list(response.data.get('results', [{}])[0].keys()) ==
            ['name', 'insee', 'url'])

    state_code = response.data.get('results', [{}])[0].get('insee', None)

    """
    Test township detail view keys
    """
    response = client.get(reverse('township-detail',
                                  args=[state_code]))

    assert response.status_code == 200
    assert list(response.data.keys()) == ['insee', 'name']

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
