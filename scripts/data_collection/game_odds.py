from game_ids import ncaab_get_todays_game_ids
import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta, timezone, time
from OddsJamClient import OddsJamClient

game_ids_df = ncaab_get_todays_game_ids()
if 'game_id' in game_ids_df.columns:
    game_ids = game_ids_df['game_id'].tolist()
else:
    print("Error: 'game_id' column not found in the DataFrame")
    game_ids = []

def get_cbb_odds(game_ids):
    desired_markets = ['Moneyline', 'Point Spread', 'Total Points']
    URL = "https://api-external.oddsjam.com/api/v2/game-odds"
    API_KEY = '540d8b29-e704-403d-9926-363d3d7fcaff'

    game_id_chunks = [game_ids[i:i + 5] for i in range(0, len(game_ids), 5)]
    processed_data = []

    for chunk in game_id_chunks:
        params = {
            'key': API_KEY,
            'sportsbook': ['Pinnacle'],
            'game_id': chunk,
            'market_name': desired_markets,
            'is_main': 'true'
        }

        response = requests.get(URL, params=params)
        if response.status_code == 200:
            games_odds = response.json()['data']
            for game in games_odds:
                game_id = game['id']
                home_team = game['home_team']
                away_team = game['away_team']
                for odds in game['odds']:
                    entry = {
                        'game_id': game_id,
                        'home_team': home_team,
                        'away_team': away_team,
                        'market_name': odds['market_name'],
                        'price': odds['price'],
                        'points': odds['bet_points']
                    }
                    # Check if the odds are for a specific selection (team) or over/under
                    if odds['selection']:
                        entry['team'] = odds['selection']
                    else:
                        entry['team'] = 'Over/Under'

                    # Determine if the entry is for the home or away team
                    if entry['team'] == home_team:
                        entry['home_or_away'] = 'home'
                    elif entry['team'] == away_team:
                        entry['home_or_away'] = 'away'
                    else:
                        entry['home_or_away'] = 'total'

                    processed_data.append(entry)
        else:
            print(f"Error {response.status_code}: {response.text}")

    # Convert to a DataFrame
    df = pd.DataFrame(processed_data)
    df = df.drop_duplicates(subset=['game_id', 'team', 'market_name'], keep='last')
    # Reshape the DataFrame to have separate columns for each type of odds
    df_moneyline = df[df['market_name'] == 'Moneyline'].pivot(index='game_id', columns='home_or_away', values='price').rename(columns={'home': 'home_moneyline', 'away': 'away_moneyline'})
    df_spread = df[df['market_name'] == 'Point Spread'].pivot(index='game_id', columns='home_or_away', values=['price', 'points']).rename(columns={'price': 'spread_odds', 'points': 'point_spread'})
    df_totals = df[df['market_name'] == 'Total Points'].pivot(index='game_id', columns='team', values=['price', 'points']).rename(columns={'price': 'total_points_odds', 'points': 'total_points'})
    
    # Merge the reshaped DataFrames back together
    df_final = df_moneyline.join([df_spread, df_totals])
    df_final.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in df_final.columns]

# Now rename the columns to have better naming convention
    df_final = df_final.rename(columns={
        'away_moneyline': 'away_moneyline_odds',
        'home_moneyline': 'home_moneyline_odds',
        'spread_odds_away': 'away_point_spread_odds',
        'spread_odds_home': 'home_point_spread_odds',
        'point_spread_away': 'away_point_spread',
        'point_spread_home': 'home_point_spread',
        'total_points_odds_Over/Under': 'over_under_odds',
        'total_points_Over/Under': 'over_under_line'
    })

    df_final.reset_index(inplace=True)
    return df_final

# Example usage
odds_df = get_cbb_odds(game_ids)
df = odds_df.merge(game_ids_df,how='left',left_on='game_id',right_on='game_id')
df = df[['game_id','home_team','away_team','away_moneyline_odds', 'home_moneyline_odds',
       'away_point_spread_odds', 'home_point_spread_odds', 'away_point_spread',
       'home_point_spread', 'over_under_odds', 'over_under_line']]
spread_df = df[['home_team','away_team','home_point_spread']]
spread_df.to_csv('data/11_16OJ.csv',index=False)