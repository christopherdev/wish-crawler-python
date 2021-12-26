import requests
import csv
import getopt
import sys

TOKEN = ""
COOKIE = ""
STOKEN = ""
SCROLLS = 10
API_URL = "https://www.wish.com/api/search"

def main(argv):
    keyword = ""  
    try:
      opts, args = getopt.getopt(argv,'hk:k:',['keyword'])
    except getopt.GetoptError:
        print("wish.py -k <keyword>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("wish.py -k <keyword>")
            sys.exit()
        elif opt in ('-k', '--keyword'):
            keyword = arg.replace(' ', '-')

    if keyword == "":
        print("Keyword is required (e.g. wish.py -k <keyword>)")
        sys.exit()

    payload = {'query':keyword,'start':0,'count':30,'only_wish_express':False,'only_local_products':False,
    'request_search_filter':False,'request_search_tags':True,'securedtouch_token': STOKEN,'transform':True}
    headers = { 'X-XSRFToken' : TOKEN, 'Content-Type' : 'application/x-www-form-urlencoded', 'Cookie' : COOKIE }

    x = 1

    with open("Wish-"+keyword+".csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'title', 'url', 'price', 'image_url', 'seller', 'seller_url', 'keyword'])
        while x <= SCROLLS:
            r = requests.post(API_URL,data = payload,headers = headers)
            data = r.json()['data']
            
            payload['start'] = int(data['next_offset'])
            #print (data)
            for result in data['results']:
                seller_url = '' 
                if 'merchant_id' in result:
                    seller_url = "https://www.wish.com/merchant/" + result['merchant_id']

                if 'commerce_product_info' in result:
                    if 'merchant_id' in result['commerce_product_info']:
                        seller_url = "https://www.wish.com/merchant/" + result['commerce_product_info']['merchant_id']

                seller = ''
                if 'merchant_info' in result:
                    seller = result['merchant_info']['title']

                image_url = ''
                if 'normal_picture' in result:
                    image_url = result['normal_picture']
                elif 'small_picture' in result:
                    image_url = result['small_picture']
                elif 'display_picture' in result:
                    image_url = result['display_picture']


                price = 0
                if 'value' in result:
                    price = result['value']
                elif 'localized_value' in result:
                    price = result['localized_value']['symbol'] + result['localized_value']['localized_value']
                elif 'localized_retail_price' in result:
                    price = result['localized_retail_price']['symbol'] + result['localized_retail_price']['localized_value']
                
                if seller_url != '' and seller != '':
                    writer.writerow([result['id'], result['name'], "https://www.wish.com/c/" + result['id'], price, image_url, seller, seller_url, keyword])

            x += 1

if __name__ == "__main__":
   main(sys.argv[1:])