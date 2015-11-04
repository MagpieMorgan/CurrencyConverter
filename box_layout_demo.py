from kivy.app import App
from kivy.lang import Builder
import currency
import time


class BoxLayoutDemo(App):
    def build(self):
        self.title = "Box Layout Demo"
        self.root = Builder.load_file('box_layout.kv')
        return self.root
    def updated_time(self):
        current_time = time.strftime("%H:%M:%S")
        self.root.ids.status.text = "Updated at " + str(current_time)

    def current_date(self):
        current_time = time.strftime("%d/%m/%Y")
        self.root.ids.date_label.text = "Today is: \n" + str(current_time)

    def convert(self, text):
        try:
            amount = float(self.root.ids.input_location.text)

            converted_number = currency.convert(amount, "AUD", "JPY")
            self.root.ids.input_home.text = converted_number
        except ValueError:
            self.root.ids.input_home.text = "-1"



BoxLayoutDemo().run()