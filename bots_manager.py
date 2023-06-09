from scrapper.bots.cruz_verde import Bot as CruzVerdeBot
from scrapper.bots.farmacias_ahumada import Bot as AhumadaBot
from scrapper.bots.farmacia_botika import Bot as BotikaBot

import re
import pandas as pd
import json

parameters = json.load(open('parameters.json', 'r'))

bots = [CruzVerdeBot(), BotikaBot()]

def format_price(s):
    numbers = re.findall(r'[\d.]+', s)
    # Elimina los puntos y convierte el string a un entero
    result = int(numbers[0].replace('.', ''))
    return result

if __name__ == "__main__":
    drugs_list = parameters['drugs']
    results_path = 'products.csv'

    df = pd.DataFrame(columns=['name', 'price', 'chain', 'searched_drug'])
    for drug in drugs_list:
        for bot in bots:
            print(f"Buscando {drug} en {bot.chain}")
            products = bot.find_generic_drug(drug)
            # bot.write_to_file(products)
            print(f"Se encontraron {len(products)} productos")
            print("-"*50)
            df_temp = pd.DataFrame(products)
            df_temp['price'] = df_temp['price'].apply(format_price)
            df_temp['chain'] = bot.chain
            df_temp['searched_drug'] = drug
            # join using concat
            df = pd.concat([df, df_temp], ignore_index=True)

    df.to_csv(results_path, index=False)

    for bot in bots:
        bot.driver.quit()
