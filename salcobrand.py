import requests

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
                "Name": data[i]["Name"],
                "Price": data[i]["Price"]
            }
            product_list.append(p)
        return product_list

    
if __name__ == "__main__":
    bot = Bot()
    print(bot.find_generic_drug("ibuprofeno"))