


# scraped df needs to have home/away_FGA, home/away_OReb, home/awayTO,home/away_FTA, home/away_points
df['total_points'] = df['home_points_game'] + df['away_points_game']

hadf['home_possessions'] = (hadf['home_field_goals_att']
                              - hadf['home_offensive_rebounds']
                              + hadf['home_turnovers']
                              + 0.44 * hadf['home_free_throws_att'])

hadf['away_possessions'] = (hadf['away_field_goals_att']
                              - hadf['away_offensive_rebounds']
                              + hadf['away_turnovers']
                              + 0.44 * hadf['away_free_throws_att'])

hadf['home_offensive_efficiency'] = 100 * (hadf['home_points_game'] / hadf['home_possessions'])
hadf['away_offensive_efficiency'] = 100 * (hadf['away_points_game'] / hadf['away_possessions'])

hadf['home_defensive_efficiency'] = 100 * ((hadf['total_points'] - hadf['home_points_game']) / hadf['home_possessions'])
hadf['away_defensive_efficiency'] = 100 * ((hadf['total_points'] - hadf['away_points_game']) / hadf['away_possessions'])

df = df[['home_team','away_team','home_defensive_efficiency', 'home_offensive_efficiency', 
                        'away_offensive_efficiency', 'away_defensive_efficiency']]