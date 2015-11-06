from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
import currency
import time


class GUI(App):
    def build(self):
        Window.size = (350, 700)
        self.title = "Currency Converter"
        self.root = Builder.load_file('GUI.kv')
        return self.root

    def on_start(self):
        self.current_date()
        self.read_config()

    def updated_time(self):
        current_time = time.strftime("%H:%M:%S")
        self.root.ids.status.text = "Updated at " + str(current_time)

    def current_date(self):
        current_time = time.strftime("%d/%m/%Y")
        self.root.ids.date_label.text = "Today is: \n" + str(current_time)

    def convert_one(self):
        try:
            country_details = currency.get_all_details()
            amount = float(self.root.ids.input_location.text)
            home_currency = self.root.ids.country_name.text
            home_currency = country_details[home_currency]
            home_currency_code = home_currency[1]
            target_currency = self.root.ids.spinner.text
            target_currency = country_details[target_currency]
            target_currency_code = target_currency[1]
            converted_number = currency.convert(amount, target_currency_code, home_currency_code)
            self.status_update(home_currency[2].strip('\n'), home_currency_code, target_currency[2].strip('\n'), target_currency_code)
            self.root.ids.input_home.text = converted_number
        except ValueError:
            self.root.ids.input_home.text = "-1"

    def convert_two(self):
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
        except ValueError:
            self.root.ids.input_location.text = "-1"

    def read_config(self):
        config_details = []
        searchfile = open("config.txt", "r", encoding="utf-8")
        first_line = searchfile.readline()
        first_line = first_line.strip('\n')
        self.root.ids.country_name.text = first_line
        for line in searchfile:
            words = [line for word in line.split(",")]
            config_details.append()
        searchfile.close()

    def status_update(self, first_location, first_code, target_location, target_code):
        status_string = (first_code + "(" + first_location + ")" + " to " + target_code + "(" + target_location + ")")
        self.root.ids.status.text = str(status_string)

GUI().run()
