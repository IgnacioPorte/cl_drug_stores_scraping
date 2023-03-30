import json
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
import gzip

class Bot:
    def __init__(self):
        self.driver = webdriver.Chrome("chromedriver.exe")

    def find_generic_drug(self, drug_name):
        product_list = []
        first_link = "https://www.cruzverde.cl/"
        self.driver.get(first_link)
        click = self.driver.find_element(By.XPATH, "//at-button/button[span=' Aceptar ']")
        click.click()
        self.driver.get(f"https://www.cruzverde.cl/search?query={drug_name}")
        for request in self.driver.requests:
            if request.response:
                if "https://api.cruzverde.cl/product-service/products/product-summary" in request.url:
                    response = request.response.body
                    response = gzip.decompress(response).decode('utf-8')
                    response = json.loads(response)

                    print(response)

                    for v in response.values():
                        product = {
                            "name": v["name"],
                            "price": v["prices"]["price-list-cl"]
                        }
                        product_list.append(product)
        return product_list

if __name__ == "__main__":
    bot = Bot()
    print(bot.find_generic_drug("ibuprofeno"))