from bots.cruz_verde import Bot as CruzVerdeBot
from bots.farmacias_ahumada import Bot as AhumadaBot
from bots.farmacia_botika import Bot as BotikaBot
from bots.salcobrand import Bot as SalcobrandBot

from dotenv import load_dotenv
import os

import re
import pandas as pd
import json

load_dotenv()

parameters = json.load(open('parameters.json', 'r'))
results_base_path = os.getenv('RESULTS_BASE_PATH') or '../data/'
driver_path = os.getenv('CHROMEDRIVER_PATH')

bots = [CruzVerdeBot(driver_path), BotikaBot(driver_path), AhumadaBot(driver_path), SalcobrandBot(driver_path)]

if __name__ == "__main__":
    drugs_list = parameters['drugs']
    results_path = f"{results_base_path}products.csv"

    df = pd.DataFrame(columns=['description', 'price', 'bioequivalent', 'image_url', 'chain', 'searched_drug'])
    for drug in drugs_list:
        for bot in bots:
            try:
                print(f"Buscando {drug} en {bot.chain}")
                products = bot.find_generic_drug(drug)
                # bot.write_to_file(products)
                print(f"Se encontraron {len(products)} productos")
                print("-"*50)
                df_temp = pd.DataFrame(products)
                df_temp['chain'] = bot.chain
                df_temp['searched_drug'] = drug
                # join using concat
                df = pd.concat([df, df_temp], ignore_index=True)
            except Exception as e:
                print(e)
                with open('error.log', 'a') as f:
                    f.write(f"Error buscando {drug} en {bot.chain}: {e}\n")
                continue

    df.to_csv(results_path, index=False)

    for bot in bots:
        # Revisar que el bot tenga el atributo driver
        if hasattr(bot, 'driver'):
            bot.driver.quit()
