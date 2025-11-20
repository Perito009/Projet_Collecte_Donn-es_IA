import requests
import pytest
from unittest.mock import patch, Mock

# Essayer d'importer l'URL/constante d'API depuis extract_api.py
try:
    from extract_api import API_BASE_URL as EXTRACT_API_URL
except Exception:
    try:
        from extract_api import BASE_URL as EXTRACT_API_URL
    except Exception:
        try:
            from extract_api import WEATHER_API_URL as EXTRACT_API_URL
        except Exception:
            EXTRACT_API_URL = "https://api.openweathermap.org/data/2.5/weather"


# Petit client testé : récupère la météo courante et renvoie un dict simplifié.
def fetch_weather(city, api_key, base_url="https://api.openweathermap.org/data/2.5/weather", timeout=5):
    params = {"q": city, "appid": api_key, "units": "metric"}
    resp = requests.get(base_url, params=params, timeout=timeout)
    resp.raise_for_status()
    data = resp.json()
    main = data.get("main", {})
    weather = (data.get("weather") or [{}])[0]  # <-- handle empty list safely
    return {"city": data.get("name"), "temp": main.get("temp"), "description": weather.get("description")}


def make_mock_response(status_code=200, json_data=None, raise_for_status_exc=None):
    mock_resp = Mock()
    mock_resp.status_code = status_code
    if raise_for_status_exc:
        mock_resp.raise_for_status.side_effect = raise_for_status_exc
    else:
        mock_resp.raise_for_status.return_value = None
    mock_resp.json.return_value = json_data if json_data is not None else {}
    return mock_resp


def test_fetch_weather_success():
    sample_api_response = {
        "name": "Paris",
        "main": {"temp": 12.3},
        "weather": [{"description": "light rain"}]
    }
    mock_resp = make_mock_response(status_code=200, json_data=sample_api_response)

    with patch("requests.get", return_value=mock_resp) as mock_get:
        result = fetch_weather("Paris", "fake-key", base_url=EXTRACT_API_URL)
        mock_get.assert_called_once()
        assert result["city"] == "Paris"
        assert isinstance(result["temp"], float) or isinstance(result["temp"], int)
        assert result["description"] == "light rain"


def test_fetch_weather_http_error():
    # Simule une erreur HTTP (401 par ex.) : raise_for_status lance HTTPError
    http_err = requests.HTTPError("401 Client Error: Unauthorized")
    mock_resp = make_mock_response(status_code=401, json_data={"message": "unauthorized"}, raise_for_status_exc=http_err)

    with patch("requests.get", return_value=mock_resp):
        with pytest.raises(requests.HTTPError):
            fetch_weather("Paris", "invalid-key", base_url=EXTRACT_API_URL)


def test_fetch_weather_timeout():
    # Simule un timeout de la requête
    with patch("requests.get", side_effect=requests.Timeout):
        with pytest.raises(requests.Timeout):
            fetch_weather("Paris", "any-key", base_url=EXTRACT_API_URL, timeout=0.1)


def test_fetch_weather_invalid_json():
    # Simule une réponse 200 mais json() lève une erreur (payload invalide)
    mock_resp = make_mock_response(status_code=200)
    mock_resp.json.side_effect = ValueError("Invalid JSON")

    with patch("requests.get", return_value=mock_resp):
        with pytest.raises(ValueError):
            fetch_weather("Paris", "any-key", base_url=EXTRACT_API_URL)


def test_fetch_weather_missing_fields():
    # Réponse OK mais champs manquants -> vérifier qu'on obtient None pour les champs absents
    minimal_response = {"name": None, "main": {}, "weather": []}
    mock_resp = make_mock_response(status_code=200, json_data=minimal_response)

    with patch("requests.get", return_value=mock_resp):
        result = fetch_weather("UnknownCity", "any-key", base_url=EXTRACT_API_URL)
        assert result["city"] is None
        assert result["temp"] is None
        assert result["description"] is None