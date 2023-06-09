from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

import csv
import time

class Bot:
    def __init__(self):
        self.chain = "Cruz Verde"
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def find_generic_drug(self, drug_name):
        product_list = []

        link = f"https://www.cruzverde.cl/search?query={drug_name}"
        self.driver.get(link)
        try:
            button_accept = WebDriverWait(self.driver, 10).until(
                lambda x: x.find_element(By.XPATH, "//at-button/button[span=' Aceptar ']")
            )
            button_accept.click()
        except:
            # Si el navegador estaba abierto, el botón no aparece
            pass
        page = 1

        while True:
            try:
                time.sleep(5)
                products = WebDriverWait(self.driver, 10).until(
                    lambda x: x.find_elements(By.CSS_SELECTOR, "div ml-card-product")
                )
                
                for product in products:
                    p = {
                        "description": WebDriverWait(product, 10).until(
                            lambda x: x.find_element(By.XPATH, "div/div/div[2]/div[2]/at-link/a").text
                        ),
                        "price": WebDriverWait(product, 10).until(
                            lambda x: x.find_element(By.XPATH, "div/div/div[3]/div/ml-price-tag/div[1]/div[1]").text.split()[1].replace(".", "")
                        ),
                        "bioequivalent": drug_name,
                        "image_url": WebDriverWait(product, 10).until(
                            lambda x: x.find_element(By.CSS_SELECTOR, "ml-product-image a > img").get_attribute("src")
                        )
                    }
                    product_list.append(p)
                page += 1
                click = WebDriverWait(self.driver, 10).until(
                    lambda x: x.find_element(By.XPATH, f"//div[text()= {page} ]")
                )
                click.click()

            except Exception as e:
                print(e)
                break

        return product_list
    
    def write_to_file(self, products_list):
        with open("data/products_cruz_verde.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["description", "price", "bioequivalent", "image_url"])
            for product in products_list:
                writer.writerow([product["description"], product["price"], product["bioequivalent"], product["image_url"]])

if __name__ == "__main__":
    bot = Bot()
    product_list = []
    with open("druglist.txt", "r") as f:
        drugs = f.readlines()
        for drug in drugs:
            product_list += bot.find_generic_drug(drug.strip())

    product_list += bot.find_generic_drug("ibuprofeno")
