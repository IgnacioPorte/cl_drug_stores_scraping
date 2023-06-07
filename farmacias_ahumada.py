from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import csv
class Bot:
    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def find_generic_drug(self, drug_name):
        self.driver.get("https://www.farmaciasahumada.cl/")
        self.driver.find_element_by_id("search").send_keys(drug_name)
        self.driver.find_element_by_id("search").submit()
        WebDriverWait(self.driver, 10).until(
            lambda x: x.find_element(By.CSS_SELECTOR, "li.product-item")
        )
        products = self.driver.find_elements(By.CSS_SELECTOR, "li.product-item")

        products_list = []

        for product in products:
            p = {
                "name": product.find_element(By.CSS_SELECTOR, ".product-brand-name").text,
                "description": product.find_element(By.CSS_SELECTOR, ".product-item-details").text.replace("\n", " "),
                "img_url": product.find_element(By.CSS_SELECTOR, ".product-image-photo").get_attribute("src")
            }
            products_list.append(p)
        return products_list
    
    def write_to_file(self, products_list):
        with open("products_ahumada.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "description", "img_url"])
            for product in products_list:
                writer.writerow([product["name"], product["description"], product["img_url"]])


if __name__ == "__main__":
    bot = Bot()
    product_list = bot.find_generic_drug("ibuprofeno")
    bot.write_to_file(product_list)