from io import open
from web_utility import load_page
import re

def convert(amount, home_currency, target_currency): #Takes the currency codes and amounts and converts them using the google finance conversion
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

def get_all_details(): #Obtains all details from the currency_details.txt.
    countries_dict = {} #Creates an empty dictionary
    searchfile = open("currency_details.txt", "r", encoding="utf-8") #Opens the currency_details.txt
    for line in searchfile: #Looks through every line
        country_details = tuple(line.split(",")) #Creates a tuple of each line, containing 3 items split by commas
        countries_dict[country_details[0]] = country_details #using the name from the first tuple item as the key, it stores the entire tuple in the dictionary
    searchfile.close() #closes the search file
    return countries_dict #Returns the dictionary to the app/function requiring it
