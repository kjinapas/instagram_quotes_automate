
import requests
from key import ninja_key
import random
category = ['success','inspirational','life','faith','dreams','hope',]


#gen quotes
query = random.choice(category)

def get_quotes():
    api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(query)
    response = requests.get(api_url, headers={'X-Api-Key': ninja_key})
    data= response.json()
    quote = data[0]['quote']
    author = data[0]['author']
    quotes = [quote,author]
    return quotes


print(get_quotes())