from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import csv
class Bot:
    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def find_generic_drug(self, drug_name):
        self.driver.get(f"https://www.farmaciasahumada.cl/catalogsearch/result/?q={drug_name}")
        WebDriverWait(self.driver, 10).until(
            lambda x: x.find_element(By.CSS_SELECTOR, "li.product-item")
        )
        products = self.driver.find_elements(By.CSS_SELECTOR, "li.product-item")

        products_list = []

        for product in products:
            full_description = product.find_element(By.CSS_SELECTOR, ".product-item-details").text.replace("\n", " ")
            description = full_description.split("$")[0].strip()
            price = full_description.split("$")[1].replace(".", "").split()[0]
            image_url = product.find_element(By.CSS_SELECTOR, ".product-image-photo").get_attribute("src")

            p = {
                "description": description,
                "price": price,
                "bioequivalent": drug_name,
                "image_url": image_url,
                "chain": "Farmacia Ahumada",
                "searched_drug": drug_name
            }
            products_list.append(p)
        return products_list
    
    def write_to_file(self, products_list):
        with open("data/products_ahumada.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["description", "price", "bioequivalent", "image_url", "chain", "searched_drug"])
            for product in products_list:
                writer.writerow([product["description"], product["price"], product["bioequivalent"], product["image_url"], product["chain"], product['searched_drug']])

if __name__ == "__main__":
    bot = Bot()
    product_list = []
    with open("druglist.txt", "r") as f:
        drugs = f.readlines()
        for drug in drugs:
            product_list += bot.find_generic_drug(drug.strip())

    bot.write_to_file(product_list)