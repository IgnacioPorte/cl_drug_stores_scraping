import requests
import json
import pandas as pd


def get_info(store_name):
    # set up the request parameters
    params = {
        'api_key': '163857A617224CD280F5E4A924D3F610',
        'search_type': 'places',
        'q': store_name,
        'location': 'Santiago,Santiago Metropolitan Region,Chile',
        'google_domain': 'google.cl',
        'gl': 'cl',
        'hl': 'es',
        'max_page': '1',
        'num': '10',
    }

    # make the http GET request to Scale SERP
    api_result = requests.get('https://api.scaleserp.com/search', params)
    return api_result.json()

drugstores = [
    'Cruz Verde',
    # 'Farmacia Ahumada',
    # 'Farmacia Botika',
]

df = pd.DataFrame(columns=['chain', 'title', 'latitude', 'longitude', 'address', 'phone'])

for drugstore in drugstores:
    data = get_info(drugstore)
    for result in data['places_results']:
        df = df.append({
            'chain': drugstore,
            'title': result['title'],
            'latitude': result['gps_coordinates']['latitude'],
            'longitude': result['gps_coordinates']['longitude'],
            'address': result['address'],
            'phone': result['phone'] if 'phone' in result else None,
        }, ignore_index=True)

df.to_csv('../data/drugstores.csv', index=False)
