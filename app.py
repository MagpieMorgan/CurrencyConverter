from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
import currency
import time


class GUI(App):
    def build(self):
        Window.size = (350, 700) #Dictates the window size to be 350 pixels wide, 700 high
        self.title = "Currency Converter" #When the app is run, the title that appears at the start
        self.root = Builder.load_file('GUI.kv') #When it runs, it uses the GUI.kv file
        return self.root

    def on_start(self): #This function runs at the start of the program, without the user's input needed
        self.current_date() #Runs the function below to obtain the current date
        self.read_config() #Reads the config to get the spinner and country information

    def current_date(self): #This function figures out the time and sets it in the label
        current_time = time.strftime("%d/%m/%Y") #The variable current_time is set to be a string of the time in DD, MM, YYYY format
        self.root.ids.date_label.text = "Today is: \n" + str(current_time) #sets the date_label to be the date across two lines

    def convert_to_home(self): #First of three conversion functions, to convert from the destination to the home currency.
        try: #Tries this block of code first, but should a Value Error appear it will act out the except ValueError code
            country_details = currency.get_all_details() #runs get_all_details in the currency.py file to obtain country codes in a dictionary
            amount = float(self.root.ids.input_location.text) #Sets the current text as a float in the location/destination text field
            home_currency = self.root.ids.country_name.text #obtains the country name from the GUI
            home_currency = country_details[home_currency] #uses the name as a key on the already obtained dictionary
            home_currency_code = home_currency[1] #Gets the country code from the result
            target_currency = self.root.ids.spinner.text #Does the same as previous 3 lines, but for the target currency
            target_currency = country_details[target_currency]
            target_currency_code = target_currency[1]
            converted_number = currency.convert(amount, target_currency_code, home_currency_code) #runs the convert function in currency.py
            self.status_update(target_currency[2].strip('\n'), target_currency_code, home_currency[2].strip('\n'), home_currency_code) #Sets the status to show the conversion and the updated time
            self.root.ids.input_home.text = converted_number #shows in the GUI text field that the currency was not entered what the conversion is
        except ValueError: #Runs if a value error appears in the above code
            self.root.ids.input_home.text = "-1" #this will be shown as the 'conversion' should a value error arise
            self.root.ids.status.text = "Error in Conversion" #this is shown in the status.

    def convert_to_location(self): #Same as previous function except inversed
        try:
            country_details = currency.get_all_details()
            amount = float(self.root.ids.input_home.text)
            home_currency = self.root.ids.country_name.text
            home_currency = country_details[home_currency]
            home_currency_code = home_currency[1]
            target_currency = self.root.ids.spinner.text
            target_currency = country_details[target_currency]
            target_currency_code = target_currency[1]
            converted_number = currency.convert(amount, home_currency_code, target_currency_code)
            self.root.ids.input_location.text = converted_number
            self.status_update(home_currency[2].strip('\n'), home_currency_code, target_currency[2].strip('\n'), target_currency_code)
        except ValueError:
            self.root.ids.input_location.text = "-1"
            self.root.ids.status.text = "Error in Conversion"

    def conversion_rates(self): #Same as the first conversion function, however always defaults to only converting 1 in the selected currency for the conversion rate rather than an actual conversion
        try:
            country_details = currency.get_all_details()
            amount = float("1")
            home_currency = self.root.ids.country_name.text
            home_currency = country_details[home_currency]
            home_currency_code = home_currency[1]
            target_currency = self.root.ids.spinner.text
            target_currency = country_details[target_currency]
            target_currency_code = target_currency[1]
            converted_number = currency.convert(amount, target_currency_code, home_currency_code)
            self.status_update(target_currency[2].strip('\n'), target_currency_code, home_currency[2].strip('\n'), home_currency_code)
            self.root.ids.input_home.text = converted_number
            self.root.ids.input_location.text = "1"
        except ValueError:
            self.root.ids.input_home.text = "-1"
            self.root.ids.status.text = "Error in Conversion"

    def read_config(self): #Reads the config
        config_details = [] #sets an empty list
        searchfile = open("config.txt", "r", encoding="utf-8") #opens the config.txt file
        for line in searchfile: #looks through each line in the file, takes the first item and adds it to the config_details list.
            words = [line for line in line.strip().split(',')]
            words = words[0]
            config_details.append(words)
        searchfile.close() #closes the file and stops searching
        home_country = config_details[0] #sets the home country to be the first line/object in the config
        self.root.ids.country_name.text = home_country #sets the home country to be the first line/object in the config
        config_details = config_details[1:] #removes the first line by resaving the rest of the list over itself.
        self.root.ids.spinner.values = config_details #sets the spinner to use the list

    def enable_text(self): #enables the text fields, called when a spinner object is selected
        self.root.ids.input_home.disabled = False
        self.root.ids.input_location.disabled = False

    def status_update(self, first_location, first_code, target_location, target_code): #updates conversion and the current time.
        current_time = time.strftime("%H:%M:%S")
        self.root.ids.status.text = "Updated at " + str(current_time)
        status_string = (first_code + "(" + first_location + ")" + " to " + target_code + "(" + target_location + ")\n" + "Updated at " + str(current_time))
        self.root.ids.status.text = str(status_string)

GUI().run() #Opens the GUI.
