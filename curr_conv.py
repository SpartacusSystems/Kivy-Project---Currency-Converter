import kivy
import requests
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder

Builder.load_file('curr_conv.kv')
# Global variable which will contain the valid currency codes
valid_codes = []

# Function to get the supported currency codes
def get_valid_codes(api_key):
    global valid_codes
    request_url = "https://v6.exchangerate-api.com/v6/" + api_key + "/codes"
    try:
        # Get data from the web API
        response = requests.get(request_url)
        # Convert the JSON data object into a Python-friendly format.
        data = response.json()
    except:
        # Possible server / internet connection issue
        print("")
        print("===> Error detected: Unable to connect to server")
        print("")


    # Store the codes in the global variable
    for code in data["supported_codes"]:
        valid_codes.append(code[0])


def get_rates(currency, api_key):
    request_url = "https://v6.exchangerate-api.com/v6/" + api_key + "/latest/" + currency

    # Get data from the web API
    response = requests.get(request_url)

    # Convert the JSON data object into a Python-friendly format.
    data = response.json()

    # Extract the conversion rates from the data object and save it to a dictionary
    rates = {}
    conv_rates = data["conversion_rates"]
    for r in conv_rates:
        rates[r] = conv_rates[r]

    # Return the extracted rates dictionary
    return rates


class MyFloatLayout(FloatLayout):
    api = ObjectProperty(None)
    rates = {}
    rate=0

    def convert(self):
        print("Yes")


    def api_changed(self):
        # Get list of valid currency codes
        try:
            get_valid_codes(self.api.text)

        except:
            print("")
            print("Invalid API key or connection issue.")
            print("Please try again...")
            print("")
            return
        self.ids.currency_from.text = "Select Currency"
        self.ids.currency_to.text = "Select Currency"
        self.ids.currency_from.values = valid_codes
        self.ids.currency_to.values = valid_codes
        #print(self.codes)

    def compute_rate(self):
        self.ids.label_rate.text = ""
        self.ids.label_rate.text = "Exchange Rate (" + self.ids.currency_from.text + " to " + self.ids.currency_to.text + "): "
        self.rates = get_rates(self.ids.currency_from.text, self.api.text)
        self.rate = self.rates[self.ids.currency_to.text]
        self.ids.exchange_rate.text = str(round(self.rates[self.ids.currency_to.text],4))

    def currency_from_clicked(self, value):
        if self.ids.currency_to.text == "Select Currency" or self.ids.currency_to.text=="":
            return
        self.compute_rate()
        self.ids.text_amt.text = ""
        self.ids.exchange_results.text = ""
        self.ids.label_results.text = ""

    def currency_to_clicked(self, value):
        if self.ids.currency_from.text == "Select Currency" or self.ids.currency_from.text=="":
            return
        self.compute_rate()
        self.ids.text_amt.text=""
        self.ids.exchange_results.text = ""
        self.ids.label_results.text = ""

    def amt_changed(self):

        if self.rate <= 0 or self.ids.text_amt.text=="":
            return
        conv_result = float(self.ids.text_amt.text) * self.rate
        self.ids.label_results.text = "Exchange Result: "
        self.ids.exchange_results.text = self.ids.text_amt.text + " " + self.ids.currency_from.text + " = " + str(round(conv_result,2)) + " " + self.ids.currency_to.text

class curr_conv(App):
    def build(self):
        return MyFloatLayout()


if __name__ == "__main__":
    curr_conv().run()