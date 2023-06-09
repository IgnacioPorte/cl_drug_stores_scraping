from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
import time
import csv

class Bot:
    def __init__(self):
        self.chain = "Farmacia Botika"
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def find_generic_drug(self, drug_name):
        product_list = []
        page = 0
        try:
            while page == 0 or products:
                page += 1
                link = f"https://farmacialabotika.cl/search?type=product&options%5Bprefix%5D=last&options%5Bunavailable_products%5D=show&q={drug_name}&page={page}"
                self.driver.get(link)
                products = self.driver.find_elements(
                    By.CSS_SELECTOR, "div.product-item")
                for product in products:
                    description = product.find_element(
                        By.CSS_SELECTOR, "div.product-item__info-inner a").text
                    price = product.find_element(
                        By.CSS_SELECTOR, "span.price--highlight").text.replace('"', "").replace('$', "").replace('.', "").split()[3]
                    try:
                        image_url = product.find_element(By.CSS_SELECTOR, "div.product-item img").get_attribute("srcset")
                    except:
                        image_url = ""
                    product_list.append({
                        "description": description,
                        "price": price,
                        "bioequivalent": drug_name,
                        "image_url": image_url
                    })


        except Exception as e:
            print(e)

        return product_list

    def write_to_file(self, products_list):
        with open("data/products_botika.csv", "w", newline="") as f:
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
    bot.write_to_file(product_list)