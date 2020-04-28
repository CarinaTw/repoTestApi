# https://www.openbrewerydb.org/

# Returns a list of breweries. -- 'https://api.openbrewerydb.org/breweries'
# by_city, by_name, by_type, page, per_page, sort

# Get a single brewery. -- 'https://api.openbrewerydb.org/breweries/5494'
# by id

# Search for breweries based on a search term. -- 'https://api.openbrewerydb.org/breweries/search?query=dog'
# NOTE: For the query parameter, you can use underscores or url encoding for spaces (%20)

import pytest


def test_returned_all_breweries(method, url):
    """ Check list returned """
    response = method(url)
    json = response.json()
    for i in json:
        for key in i.keys():
            assert not i[key] == None


@pytest.mark.parametrize("city", ['Alameda', 'Morrow', 'Catawba Island'])
def test_returned_all_breweries_by_city(method, city, url):
    """ Check returned all breweries by city """
    add_url = '?by_city=' + city
    response = method(url+add_url)
    json = list(response.json())
    for i in range(len(json)):
        assert json[i]['city'] == city


@pytest.mark.parametrize("type", ['brewpub'])
def test_returned_all_breweries_by_type(method, type, url):
    add_url = '?by_type=' + type
    response = method(url+add_url)
    json = list(response.json())
    for i in range(len(json)):
        assert json[i]['brewery_type'] == type


@pytest.mark.parametrize("page_num", [-1, 0, 1, 100, 402])
def test_returned_all_breweries_on_page_number(method, page_num, url):
    add_url = '?page=' + str(page_num)
    response = method(url+add_url)
    json = list(response.json())
    assert len(json) > 0


@pytest.mark.parametrize("page_num", [403, 10000])
def test_returned_all_breweries_on_page_number_negative(method, page_num, url):
    add_url = '?page=' + str(page_num)
    response = method(url+add_url)
    json = list(response.json())
    assert len(json) == 0


@pytest.mark.parametrize("per_p", [0, 1, 10, 50])
def test_returned_all_breweries_per_page(method, per_p, url):
    add_url = '?per_page=' + str(per_p)
    response = method(url+add_url)
    json = list(response.json())
    assert len(json) == per_p


@pytest.mark.parametrize("per_p", [-1, 51, 100])
def test_returned_all_breweries_per_page_negative(method, per_p, url):
    add_url = '?per_page=' + str(per_p)
    response = method(url+add_url)
    json = list(response.json())
    assert not len(json) == per_p


@pytest.mark.parametrize("sorted_desc_name", ['-name'])
@pytest.mark.parametrize("city", ['Alameda', 'San Diego'])
def test_returned_all_breweries_sorted_by(method, sorted_desc_name, city, url):
    add_url = '?by_city=' + city + '&sort=' + sorted_desc_name
    response = method(url+add_url)
    json = list(response.json())
    assert ord(json[0]['name'][:1]) > ord(json[len(json)-1]['name'][:1])


@pytest.mark.parametrize("id", [2, 253, 1495, 8007])
def test_returned_brewery_get(method, id, url):
    add_url = '/' + str(id)
    response = method(url+add_url)
    json = response.json()
    assert json['id'] == id