import pytest


def test_example(regions_api):
    response = regions_api.get()
    number_of_regions = response.json()['total']
    assert response.status_code == 200, f"Response status code is not 200: {response.status_code}"
    assert number_of_regions == 22, f"Count of regions is wrong: {number_of_regions}"


@pytest.mark.parametrize("page_size", [5, 10, 15])
def test_total_number_of_unique_regions(regions_api, page_size):

    all_regions = set()

    for page in range(1, 10):
        get_regions = regions_api.get(params={
            'page': page,
            'page_size': page_size
        })
        assert get_regions.status_code == 200, f"Response status code is not 200: {get_regions.status_code}"
        list_of_regions = get_regions.json()['items']
        if len(list_of_regions) == 0:
            break
        for region in list_of_regions:
            for key, value in region.items():
                if key == 'name':
                    all_regions.add(value)

    assert len(all_regions) == 21, f"Total number of unique regions is wrong: {len(all_regions)}"


@pytest.mark.parametrize("page_size, result", [(5, 26), (10, 23), (15, 22)])
def test_total_number_of_regions(regions_api, page_size, result):

    all_regions = []

    for page in range(1, 10):
        get_regions = regions_api.get(params={
            'page': page,
            'page_size': page_size
        })
        assert get_regions.status_code == 200, f"Response status code is not 200: {get_regions.status_code}"
        list_of_regions = get_regions.json()['items']
        if len(list_of_regions) == 0:
            break
        for region in list_of_regions:
            for key, value in region.items():
                if key == 'name':
                    all_regions.append(value)

    assert len(all_regions) == result, f"Total number of regions is wrong: {len(all_regions)}"


def test_default_number_of_regions_on_1_page(regions_api):
    response = regions_api.get()
    number_of_regions_on_page = response.json()['items']
    assert response.status_code == 200, f"Response is not 200: {response.status_code}"
    assert len(number_of_regions_on_page) == 15, \
        f"Number of regions on one page is not 15: {len(number_of_regions_on_page)}"


@pytest.mark.parametrize("q_value, expected_number_of_regions", [
    ("мск", 2), ("МСК", 2), ("мСк", 2), ("МсК", 2), ("мск ", 2), ("Орёл", 1), ("Орел", 0), ("Ош", 1), ("кий", 1),
    ("кии", 0), ("mos", 0), ("COW", 0), ("вфывфывфвыфвыф", 0), ("кт-Пет", 1), ("кт-", 1), ("т-П", 1), ("-Пе", 1),
    ("231312", 0), ("!@#$", 0)
])
def test_q_param_positive(regions_api, q_value, expected_number_of_regions):
    response = regions_api.get(params={
        'q': q_value
    })
    assert response.status_code == 200, f"Response status code is not 200: {response.status_code}"
    actual_number_of_regions_in_response = len(response.json()['items'])
    assert actual_number_of_regions_in_response == expected_number_of_regions, \
        f"Number of regions in response is not equal to expected: {actual_number_of_regions_in_response}"


@pytest.mark.parametrize("q_value", ["", " ", 5, 10, "!@", "а", "АЛ", "Ал", "аЛ", "ал"])
def test_q_param_not_enough_symbols(regions_api, q_value):
    response = regions_api.get(params={
        'q': q_value
    })
    assert response.status_code == 200, f"Response status code is not 200: {response.status_code}"
    error_message = response.json()['error']['message']
    assert error_message == "Параметр 'q' должен быть не менее 3 символов", \
        f"Error message is different: {error_message}"


@pytest.mark.parametrize("country_code", ['ru', 'kg', 'kz', 'cz', 'ru ', 'kg ', 'kz ', 'cz '])
def test_country_code_param_positive(regions_api, country_code):

    for page in range(1, 10):
        response = regions_api.get(params={
            'page': page,
            'country_code': country_code
        })
        assert response.status_code == 200, f"Response status code is not 200: {response.status_code}"
        if len(response.json()['items']) == 0:
            break
        all_regions_on_page = response.json()['items']
        for region in all_regions_on_page:
            country_code_in_response = region['country']
            for key, value in country_code_in_response.items():
                if key == 'code':
                    assert value == country_code, f"Region's country is not equal to required: {value}"


@pytest.mark.parametrize("country_code", ['', ' ', 'rU', 'Ru', 'RU', 'kG', 'Kg', 'KG', 'kZ', 'Kz', 'KZ', 'cZ', 'Cz',
                                          'CZ', ' ru', 'r', 'k', 'c', 'z', '!', 'ru!', 'r_u', 'r u', 'ру', 'кз',
                                          0, 5, 10, -1, -0])
def test_country_code_param_negative(regions_api, country_code):

    response = regions_api.get(params={
        'country_code': country_code
    })
    assert response.status_code == 200, f"Response status code is not 200: {response.status_code}"
    error_message_in_response = response.json()['error']['message']
    assert error_message_in_response == "Параметр 'country_code' может быть одним из следующих значений: ru, kg, kz, cz", \
        f"Error message is not equal to expected: {error_message_in_response}"


@pytest.mark.parametrize('page', [10, 100, 1000, 10000, 100000, 1000000, 100000000, 1000000000, 10000000000,])
def test_page_param_big_values(regions_api, page):
    response = regions_api.get(params={
        'page': page
    })
    assert response.status_code == 200, f"Response status code is not 200: {response.status_code}"
    number_of_items = len(response.json()['items'])
    assert number_of_items == 0, f"There are some items on page {page}, it should not be there"


@pytest.mark.parametrize('page, ', [-1, 0])
def test_page_param_negative_value(regions_api, page):
    response = regions_api.get(params={
        'page': page
    })
    assert response.status_code == 200, f"Response status code is not 200: {response.status_code}"
    error_message = response.json()['error']['message']
    assert error_message == "Параметр 'page' должен быть больше 0", \
        f"Something wrong with error message: {error_message}"


@pytest.mark.parametrize('page, ', ["", " ", "!", "#", "@", "a", "ab", "page", 0.9, 1.1])
def test_page_param_negative_scenario(regions_api, page):
    response = regions_api.get(params={
        'page': page
    })
    assert response.status_code == 200, f"Response status code is not 200: {response.status_code}"
    error_message = response.json()['error']['message']
    assert error_message == "Параметр 'page' должен быть целым числом", \
        f"Something wrong with error message: {error_message}"


@pytest.mark.parametrize("page_size,", [5, 10, 15, "5 ", "10 ", "15 ", " 5", " 10", " 15"])
def test_page_size_param_positive(regions_api, page_size):
    response = regions_api.get(params={
        'page_size': page_size
    })
    assert response.status_code == 200, f"Response status code is not 200: {response.status_code}"
    list_of_regions = response.json()['items']
    assert len(list_of_regions) == int(page_size), \
        f"Number of regions on one page is not equal to page_size value: {len(list_of_regions)}"


@pytest.mark.parametrize("page_size", [-1, 1, 4, 6, 9, 11, 14, 16, 100, 1000, 10000, 100000000000000000000000000])
def test_page_size_param_negative(regions_api, page_size,):
    response = regions_api.get(params={
        'page_size': page_size
    })
    assert response.status_code == 200, f"Response status code is not 200: {response.status_code}"
    error_response_body = response.json()['error']['message']

    assert error_response_body == "Параметр 'page_size' может быть одним из следующих значений: 5, 10, 15", \
        f"Error message in response is different: {error_response_body}"


@pytest.mark.parametrize("page_size", ["", " ", "dsa", "!#!@", 1.5, 5., "'|/\\"])
def test_page_size_param_letters(regions_api, page_size):
    response = regions_api.get(params={
        'page_size': page_size
    })
    assert response.status_code == 200, f"Response status code is not 200: {response.status_code}"
    error_response_body = response.json()['error']['message']
    assert error_response_body == "Параметр 'page_size' должен быть целым числом", \
        f"Error message in response is different: {error_response_body}"
