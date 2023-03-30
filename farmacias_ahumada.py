from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class Bot:
    def __init__(self):
        self.driver = webdriver.Chrome("chromedriver.exe")

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
                "description": product.find_element(By.CSS_SELECTOR, ".product-item-details").text,
            }
            products_list.append(p)
        return products_list


if __name__ == "__main__":
    bot = Bot()
    print(bot.find_generic_drug("ibuprofeno"))