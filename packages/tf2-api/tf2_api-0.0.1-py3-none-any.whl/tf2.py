"""
A TF2 api! (this requires a Steam Web API key. Get one [here](https://steamcommunity.com/dev/apikey))
"""
from typing import Literal
import requests

class TF2:
    def __init__(self, steam_web_api_key: str, steam_id: int, *args, **kwargs):
        """
        A TF2 api! (this requires a Steam Web API key. Get one [here](https://steamcommunity.com/dev/apikey))
        """
        self.api_key = steam_web_api_key
        self.steam_id = steam_id
        self.pypi_page = 'https://pypi.org/project/tf2-api/'
        self.github_page = 'https://github.com/DevHollo/tf2-api/'

    def get_kills_as_class(self, tf2_class: Literal['Scout', 'Heavy', 'Pyro', 'Spy', 'Medic', 'Sniper', 'Soldier', 'Engineer', 'Demoman']) -> int:
        """
        Get total kills as the specified class
        """
        try:
            response = requests.get(f"http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v2/?appid=440&key={self.api_key}&steamid={self.steam_id}&format=json")
            response.raise_for_status()
            tf2_json = response.json()
            stats = tf2_json.get('playerstats', {}).get('stats', [])
            for stat in stats:
                if stat['name'] == f'{tf2_class}.accum.iNumberOfKills':
                    return int(stat['value'])
            return 0
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return 0
        
    def get_playtime_as_class(self, tf2_class: Literal['Scout', 'Heavy', 'Pyro', 'Spy', 'Medic', 'Sniper', 'Soldier', 'Engineer', 'Demoman']) -> str:
        """
        returns in `{HOURS}:{MINUTES}:{SECONDS}` format
        """
        def seconds_to_hms(seconds: int):
            hours = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60
            return hours, minutes, seconds
        try:
            response = requests.get(f"http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v2/?appid=440&key={self.api_key}&steamid={self.steam_id}&format=json")
            response.raise_for_status()
            tf2_json = response.json()
            stats = tf2_json.get('playerstats', {}).get('stats', [])
            for stat in stats:
                if stat['name'] == f'{tf2_class}.accum.iPlayTime':
                    time = seconds_to_hms(int(stat['value']))
                    hours = str(time[0]).zfill(2)
                    minutes = str(time[1]).zfill(2)
                    seconds = str(time[2]).zfill(2)
                    return f"{hours}:{minutes}:{seconds}"
            return "00:00:00"
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return "00:00:00"