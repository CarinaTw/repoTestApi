# https://jsonplaceholder.typicode.com/

# Get a resource -- 'https://jsonplaceholder.typicode.com/posts/1'
# List all resources -- 'https://jsonplaceholder.typicode.com/posts'
# Create a resource -- ('https://jsonplaceholder.typicode.com/posts', {
#     method: 'POST',
#     body: JSON.stringify({
#       title: 'foo',
#       body: 'bar',
#       userId: 1
#     }),
#     headers: {
#       "Content-type": "application/json; charset=UTF-8"
#     }
#   })
#

import pytest
import requests
import re

ur = 'https://jsonplaceholder.typicode.com'
@pytest.mark.parametrize("source, id", [ ('/posts/', 1), ('/albums/', 1), ('/users/', 1), ('/users/', 10) ])
def test_get_all_resources(method, source, id, url):
    response = method(url + source + str(id))
    json = response.json()

    if source == '/posts/':
        assert json['userId'] == id and "body" in list(json)
    elif source == '/albums/':
        assert json['userId'] == id and "title" in list(json) and not "body" in list(json)
    elif source == '/users/':
        assert json['id'] == id and "username" in list(json)


@pytest.mark.parametrize("source", ['/posts', '/albums', '/users'])
def test_list_all_resources(method, source, url):
    response = method(url + source)
    json = response.json()
    assert len(list(json)) > 1


@pytest.mark.parametrize("u_id", [1, 333, 1000])
def test_create_resource(u_id, method, url):
    add_url = '/posts'

    # запустить прокси
    proxies = {
        'http': 'http://localhost:8080',
        'https': 'http://localhost:8080'
    }

    data = {
            'title': 'foo',
            'body': 'bar',
            'userId': u_id
        }

    headers = {
        "Content-type": "application/json; charset=UTF-8"
    }

    response = requests.post('https://jsonplaceholder.typicode.com'+add_url, json=data,
                             headers=headers, proxies=proxies, verify=False)

    assert re.search(r'userId.\:.' + str(u_id), response.text)
