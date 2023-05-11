import requests

def test_url(url, code):
    result = requests.get(url)
    print(result)
    assert code == str(result.status_code)
