import pytest
import requests

base_url = "https://api.openbrewerydb.org/v1/"


class TestBrewery():

    @pytest.mark.parametrize("num_breweries, expected_num_breweries", [(100, 100), (0, 0)],
        ids=["positive", 'zero'])
    def test_return_list_breweries(self, num_breweries, expected_num_breweries):
        """Test returning a list of breweries"""
        url = base_url + f"/breweries?per_page={num_breweries}"
        result = requests.get(url).json()
        assert len(result) == expected_num_breweries, "It must be another number of breweries"

    @pytest.mark.parametrize("id_brewery, expected_name_brewery", [
        ('5128df48-79fc-4f0f-8b52-d06be54d0cec', '(405) Brewing Co'),
        ('9c5a66c8-cc13-416f-a5d9-0a769c87d318', '(512) Brewing Co'),
        ('ef970757-fe42-416f-931d-722451f1f59c', '10 Barrel Brewing Co')],
                             ids=["brewery_1", 'brewery_2', 'brewery_3'])
    def test_brewery_by_id(self, id_brewery, expected_name_brewery):
        """Test getting a single brewery"""
        url = base_url + f"breweries/{id_brewery}"
        result = requests.get(url)
        assert result.status_code == 200
        check = result.json()
        assert check.get("name") == expected_name_brewery
        print(check.get("name"))


    @staticmethod
    def test_random_brewery():
        """Check getting random brewery"""
        url = base_url + f"/breweries/random"
        result = requests.get(url)
        check = result.json()
        assert result.status_code == 200
        print("Status code 200") if result.status_code == 200 else f'Status code {result.status_code}'
        assert len(check) == 1

    @pytest.mark.parametrize("city, pages", [('San Diego', 10), ('Norman', 0)], ids=["San Diego", 'Norman'])
    def test_filter_by_city_pages(self, city, pages):
        """Test filter breweries by city and number of pages"""
        url = base_url + f"breweries?by_city={city.lower()}&per_page={pages}"
        result = requests.get(url)
        print(f"Статус код: {result.status_code}")
        check = result.json()
        assert len(check) == pages
        print(f'The number of requested breweries matches the expected number: {pages}')
        for f in check:
            if f == 'city':
                assert check.get('city') == city
                print(f'The name of the city matches the requested: {city}')


    @pytest.mark.parametrize('country, expected_total_num', [('united_states', '7933'), ('south_korea', '61')], ids=['USA', 'South Korea'])
    def test_metadata_brewery(self, country, expected_total_num):
        """Test getting metadata"""
        url = base_url + f'breweries/meta?by_country={country}'
        result = requests.get(url)
        print(f"Статус код: {result.status_code}")
        check = result.json()
        assert check.get('total') == expected_total_num
        print(f'In {country} is {expected_total_num} of breweries')
