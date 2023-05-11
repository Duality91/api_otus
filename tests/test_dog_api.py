import pytest
import requests

base_url = "https://dog.ceo/api/"


class TestDogApi():

    @staticmethod
    def test_random_dog_photo():
        """Тест получения рандомной фотографии собаки"""
        url = base_url + "breeds/image/random"
        result = requests.get(url)
        print(f"Статус код: {result.status_code}")
        assert result.status_code == 200
        print(f"Изображение получено. Стутус-код {result.status_code}") if result.status_code == 200 else f"Провал! Изображение не получено: код {result.status_code}"
        check = result.json()
        check_res_info = check.get("message")
        assert ".jpg" in check_res_info, "It`s not image"

    @pytest.mark.parametrize("breed, expected_list_breads", [
        ("bulldog", ['boston', 'english', 'french']),
        ("hound", ['afghan', 'basset', 'blood', 'english', 'ibizan', 'plott', 'walker']),
        ("segugio", ['italian'])
        ],
        ids=["bulldog", "hound", "segugio"])
    def test_get_list_of_subbread(self, breed, expected_list_breads):
        """Тестирование списка подпород собак"""
        url = base_url + f"breed/{breed}/list"
        result = requests.get(url)
        assert result.status_code == 200
        check = result.json()
        check_res_info = check.get("message")
        assert check_res_info == expected_list_breads, 'Result does not match the expected list of dog subbreeds'

    @pytest.mark.parametrize("breed, expected_num_photos", [
        ("bulldog", 324), ("hound", 808), ("segugio", 2)
        ], ids=["bulldog", "hound", "segugio"])
    def test_get_photos_of_bread(self, breed, expected_num_photos):
        """Получение всех фото собак породы"""
        url = base_url + f"breed/{breed}/images"
        result = requests.get(url)
        print(f"Статус код: {result.status_code}")
        assert result.status_code == 200
        check = result.json()
        num_photos = len(check.get("message"))
        assert num_photos == expected_num_photos, "Number of photos of this breed doesn`t match the expected number"

    @pytest.mark.parametrize("num_of_photos, expected_num_photos", [(3, 3), (51, 50), (0, 0)], ids=["three", "overnumber", "zero"])
    def test_multiple_random_dog_photos(self, num_of_photos, expected_num_photos):
        """Тест получения заданного количества фото собак, проверка некорректный и граничных значений"""
        url = base_url + f"breeds/image/random/{num_of_photos}"
        result = requests.get(url)
        print(f"Статус код: {result.status_code}")
        assert result.status_code == 200
        check = result.json()
        num_photos_json = len(check.get("message"))
        assert num_photos_json == expected_num_photos, 'Reflected correct num of photos'

    @staticmethod
    @pytest.mark.parametrize("breeds", ['papillon', 'pekinese', 'samoyed', 'waterdog'])
    def test_multiple_random_dog_photos(breeds):
        """Тест показа всех пород собак"""
        url = base_url + f"breeds/list/all"
        result = requests.get(url)
        print(f"Статус код: {result.status_code}")
        assert result.status_code == 200
        check = result.json()
        check_res_info = check.get('message')
        assert len(check_res_info) > 10, 'List of breeds should be longer'
        assert f'{breeds}' in check_res_info, 'List of breeds might contain all breeds from parametrize'


