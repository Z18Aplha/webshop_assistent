import requests
from pushover import Client
import yaml
from time import sleep

# PUSHOVER
USER_KEY = None
API_TOKEN = None
PUSHOVER_CLIENT = None

TIMEOUT = 60

def get_config():
    c = None  # dict with config
    with open("config.yaml", 'r') as f:
        c = yaml.load(f)
    if c is None:
        print("config not readable")
    c = replace_umlaute(c)
    return c

def replace_umlaute(c):
    for key in c["products"]:
        c["products"][key]["name"] = c["products"][key]["name"].replace("Ã¤", "ä")
        c["products"][key]["string"] = c["products"][key]["string"].replace("Ã¤", "ä")
        c["products"][key]["name"] = c["products"][key]["name"].replace("Ã¶", "ö")
        c["products"][key]["string"] = c["products"][key]["string"].replace("Ã¶", "ö")
        c["products"][key]["name"] = c["products"][key]["name"].replace("Ã¼", "ü")
        c["products"][key]["string"] = c["products"][key]["string"].replace("Ã¼", "ü")
    return c

def setup_pushover(pushover_dict):
    global USER_KEY
    USER_KEY = pushover_dict['user_key']
    global API_TOKEN
    API_TOKEN = pushover_dict['api_token']

def send_pushover(title, message):
    if USER_KEY is None or API_TOKEN is None:
        print("missing pushover credentials")
        return -1
    global PUSHOVER_CLIENT
    if PUSHOVER_CLIENT is None:  
        PUSHOVER_CLIENT = Client(USER_KEY, api_token=API_TOKEN)
    
    PUSHOVER_CLIENT.send_message(f"{message}", title=f"{title}")
    print("sent pushover")

def check_product(product):
    str_to_find = product["string"]

    r = requests.get(product["website"])
    if r.status_code == 200:
        str_found = str_to_find in r.text
        if product["indicates_in_stock"]:
            available = str_found 
        else:
            available = not str_found 
        print(f'{product["name"]} - {available}')
    else:
        print(f'web request failed ({r.status_code})')
        return -1
    return available

def main():
    c = get_config()
    setup_pushover(c['pushover'])
    products = c["products"]

    in_stock_prev = {products[p]["name"]:False for p in products}
    
    while True:
        
        in_stock = {}
        i = 0
        for key in products:
            if i == 0:
                i += 1
            else:
                sleep(3)
            in_stock[products[key]["name"]] = check_product(products[key])
        i = 0
        
        # log products in stock
        s = ''
        for i, p in enumerate(in_stock):
            if in_stock[p] == True:
                s += f'{p}'
                if i != len(in_stock)-1:
                    s += ', '
        print(f'in stock: {s}')

        # products their status changer
        s2 = ''
        if len(in_stock_prev) == len(in_stock):
            for p in in_stock:
                if in_stock[p] == in_stock_prev[p]:
                    # products status not changed
                    print(f"{p} status not changed")
                    continue
                elif in_stock[p]:
                    # products status changed to "in stock"
                    s2 += f"NEW {p} \n"
                    print(f"{p} status changed to: in stock")
                else:
                    # products status changed to "out of stock"
                    s2 += f"DIS {p}\n"
                    print(f"{p} status changed to: out of stock")

        if len(s2) > 0:
            print('stock changed')
            send_pushover('webshop assistent', f'{s2}\nin stock: {s}')

        in_stock_prev = in_stock
        sleep(TIMEOUT)


if __name__== "__main__":
    main()
