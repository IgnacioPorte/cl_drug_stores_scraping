import requests
import csv
class Bot:
    def __init__(self):
        pass

    def find_generic_drug(self, drug_name):
        product_list = []
        link = f"https://api.retailrocket.net/api/2.0/recommendation/Search/602bba6097a5281b4cc438c9/?&phrase={drug_name}&session=64257f96e44be4c7ab85ac6e&pvid=613355162587369&isDebug=false&format=json"
        response = requests.get(link)
        data = response.json()
        for i in range(len(data)):
            p = {
                "description": data[i]["Name"],
                "price": data[i]["Price"],
                "bioequivalent": drug_name,
                "image_url": data[i]["PictureUrl"],
                "chain": "Salcobrand",
                "searched_drug": drug_name
            }
            product_list.append(p)
        return product_list

    def write_to_file(self, products_list):
        with open("data/products_salcobrand.csv", "w", newline="") as f:
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