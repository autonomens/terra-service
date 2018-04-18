from django.urls import reverse


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
