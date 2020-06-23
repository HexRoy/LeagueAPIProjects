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
DevelopmentAPIKey = "RGAPI-c101c71f-cf64-4bb6-8a1d-f9dd38943108"


# ==========================================================================================
#       Home Screen: Contains summoner lookup, region selection, and favorites
# ==========================================================================================
class HomeGui(Screen):

    # Variables pulled from from <HomeGui> leaguelookup.kv
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
            popup = InvalidSearchPopup()
            popup.open_popup_1()
            print("change Region")
        elif self.summoner_name.text == "":
            popup = InvalidSearchPopup()
            popup.open_popup_2()
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
                popup = InvalidSearchPopup()
                popup.open_popup_3()
                print("no summoner " + self.summoner_name.text + " found in region: " + region)

    # Todo
    #   Check if already on favorites
    #       If not, add to bottom of grid layout and remove from search history grid layout.
    #       Reposition search history grid layout
    def add_favorite(self):
        pass

    # Todo
    #   Remove off of the layout and reposition the others
    #       Open file, keep all names except the one that was unselected. Rewrite and save the file
    #       Pandas makes this easy
    def remove_favorite(self):
        pass


# ==========================================================================================
#       Invalid Search Popup: Displays popups for bad searches
#           Types:  1 = No region selected
#                   2 = No summoner name input
#                   3 = Bad search: the combination is not found
# ==========================================================================================
class InvalidSearchPopup(FloatLayout):
    # Variables pulled from from <HomeGui> leaguelookup.kv
    popup_label = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(FloatLayout, self).__init__(**kwargs)
        self.popup = Popup(title="Error!", content=self, size_hint=(.3, .3), auto_dismiss=True)

    def open_popup_1(self):
        self.popup_label.text = "Select a region"
        self.popup.open()

    def open_popup_2(self):
        self.popup_label.text = "Enter a summoner name"
        self.popup.open()

    def open_popup_3(self):
        self.popup_label.text = "Summoner not found"
        self.popup.open()

    def close_popup(self):
        self.popup.dismiss()


# ==========================================================================================
#       Profile Gui: Overview of the searched summoner. Rank, win rate, match history
# Todo
#   Add favorite star to remove/add to favorites from their profile
# ==========================================================================================
class ProfileGui(Screen):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.name = "profile"


# ==========================================================================================
#       All Champions Gui: List of all champion stats from the current season
# ==========================================================================================
class AllChampionsGui(Screen):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)


# ==========================================================================================
#       Single Champion Gui: All stats about a single champion the summoner plays
# ==========================================================================================
class SingleChampionGui(Screen):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)


# ==========================================================================================
#       Gui Manager:
# ==========================================================================================
class GuiManager(ScreenManager):
    pass


class Summoner:
    def __init__(self):
        self.region = None
        self.name = None


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


# Todo
#   to add or remove summoner name from favorites for easy lookup
#   implement add/remove favorite
#   Add different errors to invalid lookup: no name/ region/ invalid
