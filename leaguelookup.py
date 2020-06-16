# Testing out the Riot Game League of Legends API
#       - Geoffroy Penny

import summoner_lookup
import kivy
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
import requests


# Key needed to lookup summoner information with riot's api
DevelopmentAPIKey = "RGAPI-94124332-511c-471d-a66d-974fc79f3b65"


# ==========================================================================================
#       Home Screen: Contains summoner lookup, region selection, and favorites
# ==========================================================================================
class HomeGui(Screen):

    # Pulled from leaguelookup.kv
    summoner_name = ObjectProperty(None)
    region_selection = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

    def check_summoner_name(self):
        """
         check_summoner_name

         Checks to see if a user with the name entered exists in the region selected
        :return:
        """

        # For converting region name to Platform Routing Value
        region_conversion = {
            "BR": "BR1",
            "EUN": "EUN1",
            "EUW": "EUW1",
            "JP": "JP1",
            "KR": "KR",
            "LA1": "LA1",
            "LA2": "LA2",
            "NA": "NA1",
            "OC": "OC1",
            "TR": "TR1",
            "RU": "RU"
        }

        # To make sure there is an input: Checks for region and summoner name
        #   self refers to the home screen object where data is entered, not summoner_1
        if self.region_selection.text == "Region":
            invalid_search()
            print("change Region")
        elif self.summoner_name.text == "":
            invalid_search()
            print("change sum name")
        else:       # There is data in both entries, now we test if the summoner exists
            region = region_conversion[self.region_selection.text]

            # URL to lookup a summoners basic data
            url = "https://" + region + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + \
                  self.summoner_name.text + "?api_key=" + DevelopmentAPIKey
            url_data = requests.get(url)
            code = url_data.status_code

            # Checks to see if the enter summoner name is valid in that region
            if code == 200:
                summoner_1.region = region
                summoner_1.name = self.summoner_name
                self.parent.current = "profile"
            else:
                invalid_search()
                print("no summoner " + self.summoner_name.text + " found in region: " + region)

    # Todo
    #   implement add/remove favorite
    #   to add or remove summoner name from favorites for easy lookup
    def add_favorite(self):
        pass

    def remove_favorite(self):
        pass


class InvalidSearchPopup(FloatLayout):
    def __init__(self, **kwargs):
        super(FloatLayout, self).__init__(**kwargs)

class ProfileGui(Screen):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.name = "profile"

class AllChampionsGui(Screen):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)


class SingleChampionGui(Screen):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)


class GuiManager(ScreenManager):
    pass


class Summoner:
    def __init__(self):
        self.region = None
        self.name = None


# ==========================================================================================
#       Invalid Search Popup: Displays popups for bad searches
#           Types:   No region selected
#                    No summoner name input
#                    Bad search: the combination is not found
# ==========================================================================================
def invalid_search():
    show = InvalidSearchPopup()
    popup = Popup(title="Invalid", content=show, size_hint=(.3, .3), auto_dismiss=False)
    popup.open()


# ==========================================================================================
#       The startup code
# ==========================================================================================

summoner_1 = Summoner()

kv = Builder.load_file("leaguelookup.kv")


class leaguelookupApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    leaguelookupApp().run()
