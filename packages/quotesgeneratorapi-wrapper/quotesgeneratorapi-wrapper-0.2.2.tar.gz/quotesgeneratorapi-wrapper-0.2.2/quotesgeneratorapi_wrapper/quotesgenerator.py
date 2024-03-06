import requests
import json


def getQuotes(category, api_key):
    api_url = f'https://api.api-ninjas.com/v1/quotes?category={category}'
    response = requests.get(api_url, headers={'X-Api-Key': api_key})
    if response.status_code == requests.codes.ok:
        data = response.json()
        quote = data[0]["quote"]
        author = data[0]["author"]
        content = f"{quote}\n\n{author}"
        return content
    else:
        print("Error:", response.status_code, response.text)


if __name__ == "__main__":
    try:
        api_key = input("Input API-key: ")
        getQuotes(category="happiness", api_key=api_key)
    except:
        pass
