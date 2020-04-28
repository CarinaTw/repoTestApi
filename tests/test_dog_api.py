# LIST ALL BREEDS -- https://dog.ceo/api/breeds/list/all

# DISPLAY SINGLE RANDOM IMAGE FROM ALL DOGS COLLECTION -- https://dog.ceo/api/breeds/image/random

# DISPLAY MULTIPLE RANDOM IMAGES FROM ALL DOGS COLLECTION -- https://dog.ceo/api/breeds/image/random/3
# >> Max number returned is 50.

# Run tests => pytest test_dog_api.py --url=https://dog.ceo/api

import pytest
import re


class TestDogApi:

    def __init__(self, url, method):
        response = method(url + '/breeds/list/all')
        self.lst_of_breeds = list(response.json()['message'])
        assert len(self.lst_of_breeds) == 94


def test_list_all_breeds_correct_sorted(url, method):
    """ Check list sort """

    dogapi = TestDogApi(url=url, method=method)
    assert dogapi.lst_of_breeds[0][:1] == 'a'


@pytest.mark.parametrize("code", [200])
@pytest.mark.parametrize("add_url", ['/breeds/list/all'])
def test_list_all_breeds_url_status(url, code, method, add_url):
    """ Check returned OK status """

    response = method(url + add_url)
    assert response.status_code == code


@pytest.mark.parametrize("first_part, middle_part, end_part", [('affenpinscher', 'komondor', 'wolfhound'),
                                                ('beagle', 'mastiff', 'spaniel')])
def test_list_all_breeds_existed_elemets(url, method, first_part, middle_part, end_part):
    """ Check existing correct breeds in list """
    dogapi = TestDogApi(url=url, method=method)

    assert first_part in dogapi.lst_of_breeds and \
        middle_part in dogapi.lst_of_breeds and \
        end_part in dogapi.lst_of_breeds


@pytest.mark.parametrize("param", ['apple', 'pear', 'mellon'])
def test_list_all_breeds_not_a_breed(url, method, param):
    """ Check if there are no names in the list that doesn't belong to breeds """
    dogapi = TestDogApi(url=url, method=method)

    assert not param in dogapi.lst_of_breeds


def test_return_random_img_from_all_dogs(url, method):
    """ Check dog's breed in img name match a dog's breed in the list"""
    dogapi = TestDogApi(url=url, method=method)

    r = method(url + '/breeds/image/random')
    img_url = r.json()['message']
    dogs_from_img_filename = re.split(r'/', img_url)[4]

    req_all = method(url + '/breeds/list/all')

    if re.search(r'-', dogs_from_img_filename):
        dogs_breed = re.split(r'-', dogs_from_img_filename)[0]
        dogs_subbreed = re.split(r'-', dogs_from_img_filename)[1]
        list_subbreed = req_all.json()['message'][dogs_breed]

        print('\ndogs breed  ' + dogs_breed)
        print('dogs sub-breed  ' + dogs_subbreed)

        assert dogs_breed in dogapi.lst_of_breeds and \
            dogs_subbreed in list_subbreed

    else:
        dogs_breed = dogs_from_img_filename
        req_all.json()['message'][dogs_breed]
        print('\nonly dogs breed  ' + dogs_breed)
        assert dogs_breed in dogapi.lst_of_breeds


@pytest.mark.parametrize("number", [1, 25, 50])
def test_check_max_number_returned_positive(url, method, number):
    """ Check dog's breed in img name match a dog's breed in the list"""

    r = method(url + '/breeds/image/random' + '/' + str(number))
    img_url_list = r.json()['message']
    assert len(img_url_list) == number


@pytest.mark.parametrize("number", [-1, -50, 0])
def test_check_max_number_returned_negative(url, method, number):
    """Check dog's breed in img name match a dog's breed in the list"""

    r = method(url + '/breeds/image/random' + '/' + str(number))
    img_url_list = r.json()['message']
    assert not len(img_url_list) == number
