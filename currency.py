from io import open
from web_utility import load_page
import re

def convert(amount, home_currency, target_currency):
    try:
        if home_currency == target_currency:
            return "-1"
        else:
            url_string = "https://www.google.com/finance/converter?a=%s&from=%s&to=%s" % (amount, home_currency, target_currency)
            result = load_page(url_string)
            returned_numbers = re.findall('\d+.\d+|\d+', (result[result.index("result"):]))[:2]
            if float(returned_numbers[0] or returned_numbers[1]) == amount:
                return returned_numbers[1]
            else:
                return "-1"
    except ValueError:
        return "-1"

def get_all_details():
    countries_dict = {}
    searchfile = open("currency_details.txt", "r", encoding="utf-8")
    for line in searchfile:
        country_details = tuple(line.split(","))
        countries_dict[country_details[0]] = country_details
    searchfile.close()
    return countries_dict

def get_details(country_name):
    file = open('currency_details.txt', encoding='utf-8')
    for line in file:
        words = [word for word in line.strip().split(',')]
        if words[0] == country_name:
            file.close()
            return tuple(words)
    file.close()
    return ()
