from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import csv

class Bot:
    def __init__(self):
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
                    name = product.find_element(
                        By.CSS_SELECTOR, "div.product-item__info-inner a").text
                    price = product.find_element(
                        By.CSS_SELECTOR, "span.price--highlight").text
                    product_list.append({
                        "name": name,
                        "price": price
                    })


        except Exception as e:
            print(e)

        return product_list

    def write_to_file(self, products_list):
        with open("products_botika.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "price"])
            for product in products_list:
                writer.writerow([product["name"], product["price"]])


if __name__ == "__main__":
    bot = Bot()
    product_list = bot.find_generic_drug("ibuprofeno")
    bot.write_to_file(product_list)
