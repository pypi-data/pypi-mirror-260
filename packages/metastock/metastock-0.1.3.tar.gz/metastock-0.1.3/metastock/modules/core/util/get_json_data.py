import requests


def get_json_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        json_data = response.json()  # Parse JSON from the response
        return json_data
    except Exception as e:
        print("Error:", e)
        return None
