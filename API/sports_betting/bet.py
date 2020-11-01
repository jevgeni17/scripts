#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests


#https://the-odds-api.com/
API_KEY = ''


# Get a list of in-season sports
sports_response = requests.get('https://api.the-odds-api.com/v3/sports', params={
    'api_key': API_KEY
})

sports_json = json.loads(sports_response.text)

"""if not sports_json['success']:
    print(
        'There was a problem with the sports request:',
        sports_json['msg']
    )

else:
    print()
    print(
        'Successfully got {} sports'.format(len(sports_json['data'])),
        'Here\'s the first sport:'
    )
    print(sports_json['data'])"""



# To get odds for a specific sport, use the sport key from the last request
#   or set sport to "upcoming" to see live and upcoming across all sports
SPORT_KEY = 'soccer_uefa_champs_league'

odds_response = requests.get('https://api.the-odds-api.com/v3/odds', params={
    'api_key': API_KEY,
    'sport': SPORT_KEY,
    'region': 'eu', # uk | us | eu | au
    'mkt': 'h2h' # h2h | spreads | totals
})

odds_json = json.loads(odds_response.text)
if not odds_json['success']:
    print(
        'There was a problem with the odds request:',
        odds_json['msg']
    )

else:
    # odds_json['data'] contains a list of live and 
    #   upcoming events and odds for different bookmakers.
    # Events are ordered by start time (live events are first)
   # print()
   #print(
   #     'Successfully got {} events'.format(len(odds_json['data']))
   # )
    print(odds_json['data'])

    # Check your usage
   # print()
   # print('Remaining requests', odds_response.headers['x-requests-remaining'])
    #print('Used requests', odds_response.headers['x-requests-used'])
