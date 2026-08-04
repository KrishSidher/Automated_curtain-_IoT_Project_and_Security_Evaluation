import requests
from config_reader import json_to_dict

config = json_to_dict()
latitude = config["latitude"]
longitude = config["longitude"]

def APIResponse():
    response = requests.get(f"https://api.sunrise-sunset.org/v2?lat={latitude}&lng={longitude}")
    if response.status_code == 200:
        data = response.json()
        return {
            "sunrise": data['sunrise'],
            "sunset": data['sunset']
        }
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None
