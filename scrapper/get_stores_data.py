import requests
import json
import pandas as pd

from dotenv import load_dotenv
import os

load_dotenv()
results_base_path = os.getenv('RESULTS_BASE_PATH') or '../data/'

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
        'max_page': '5',
        'num': '10',
    }

    # make the http GET request to Scale SERP
    api_result = requests.get('https://api.scaleserp.com/search', params)
    return api_result.json()

drugstores = [
    'Farmacia Ahumada',
    'Farmacia Botika',
    'Salcobrand',
    'Cruz Verde',
]

df = pd.DataFrame(columns=['chain', 'title', 'latitude', 'longitude', 'address', 'phone'])

for drugstore in drugstores:
    data = get_info(drugstore)
    try:
        for result in data['places_results']:
            new_row = pd.DataFrame([{
                'chain': drugstore,
                'title': result['title'] if 'title' in result else None,
                'latitude': result['gps_coordinates']['latitude'] if 'latitude' in result['gps_coordinates'] else None,
                'longitude': result['gps_coordinates']['longitude'] if 'longitude' in result['gps_coordinates'] else None,
                'address': result['address'] if 'address' in result else None,
                'phone': result['phone'] if 'phone' in result else None, # No testeado
            }])
            df = pd.concat([df, new_row], ignore_index=True)
    except Exception as e:
        print(e)
        with open('error.log', 'a') as f:
            f.write(f"Error buscando {drugstore}: {e}\n")
        continue

df.to_csv(f'{results_base_path}/drugstores.csv', index=False)
