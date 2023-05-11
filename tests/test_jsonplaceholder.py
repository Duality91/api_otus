import pytest
import requests

base_url = "https://jsonplaceholder.typicode.com/"


class TestJson():

    @staticmethod
    def test_json_list():
        """Test getting list of posts"""
        url = base_url + "posts"
        result = requests.get(url)
        print(f"Статус код: {result.status_code}")
        assert result.status_code == 200
        assert len(result.json()) == 100
        print(f'List of posts consist of {len(result.json())} elements')


    @pytest.mark.parametrize("body, expected_title", [
        ({'title': 'foo', 'body': 'bar', 'userId': 1}, 'foo'), ({'title': 'bird', 'body': 'sky', 'userId': 8}, 'bird')],
        ids=["foo", "bird"])
    def test_creation_resource(self, body, expected_title):
        """Test resource creation"""
        url = base_url + 'posts'
        headers = {
            'Content-type': 'application/json; charset=UTF-8',
            }
        result = requests.post(url, body, headers)
        print(f"Статус код: {result.status_code}")
        assert result.status_code == 201
        check = result.json()
        assert check.get('title') == expected_title
        print(f"Title of new object is {check.get('title')}, userId: {check.get('userId')}")

    def test_updating_resource(self):
        """Test updating resource"""
        url = base_url + 'posts/1'
        body = {'id': 1,
            'title': 'foo',
            'body': 'bar',
            'userId': 1,
            }
        headers = {
        'Content-type': 'application/json; charset=UTF-8',
        }
        result = requests.put(url, body) #Почему-то не принимает 3 агрумента, шлю запрос без заголовков
        print(f"Статус код: {result.status_code}")
        assert result.status_code == 200
        check = result.json()
        assert check.get('id') == 1 and check.get('userId') == '1'

    def test_deletind_resource(self):
        url = base_url + 'posts/1'
        result = requests.delete(url)
        print(f"Статус код: {result.status_code}")
        assert result.status_code == 200
        check = result.json()
        assert check == {}
        print('Data is empty')


    @pytest.mark.parametrize("user_id", [1, 5, 10], ids=['user_1', 'user_2', 'user_3'])
    def test_filter_posts(self, user_id):
        url = base_url + f'posts?userId={user_id}'
        result = requests.get(url)
        print(f"Статус код: {result.status_code}")
        assert result.status_code == 200
        check = result.json()
        assert len(check) == 10 #Проверяем количество выданных результатов
        for list_posts in check:
            assert list_posts.get('userId') == user_id
        print(f'All posts have User Id № {user_id}')

