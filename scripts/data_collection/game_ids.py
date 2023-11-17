import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta, timezone, time
from OddsJamClient import OddsJamClient

def ncaab_get_todays_game_ids():
    # Initialize the client (assuming you have a client setup)
    Client = OddsJamClient('540d8b29-e704-403d-9926-363d3d7fcaff')  # Replace 'your_api_key' with your actual API key
    Client.UseV2()

    # Get games for the league
    GamesResponse = Client.GetGames(league='ncaab')
    Games = GamesResponse.Games

    # Parse the game data
    parsed_games = []
    for game in Games:
        # Access the attributes of the Game object directly
        game_id = getattr(game, 'id', None)
        home_team = getattr(game, 'home_team', None)
        away_team = getattr(game, 'away_team', None)
        parsed_games.append({'game_id': game_id, 'home_team': home_team, 'away_team': away_team})

    # Create DataFrame
    df = pd.DataFrame(parsed_games)

    return df
