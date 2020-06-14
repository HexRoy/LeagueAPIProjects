# Testing out the Riot Game League of Legends API
#       - Geoffroy Penny

import summoner_lookup
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder

# Key needed to lookup summoner information with riot's api
DevelopmentAPIKey = "RGAPI-f20f5a7c-bc0a-437d-8883-4fc71d3ac3ad"


class HomeGui(Screen):
    summoner_name = ObjectProperty(None)
    region_selection = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

    def check_summoner_name(self):
        # Converts region name to Platform Routing Value
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
        if self.region_selection.text == "Region":
            print("change Region")
        elif self.summoner_name.text == "":
            print("change sum name")
        else:
            region = region_conversion[self.region_selection.text]
            print(region)
            print(self.summoner_name.text)

            summoner_1.region = region

        # url = "https://" + region + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + name + \
        #       "?api_key=" + DevelopmentAPIKey

       # self.parent.current = "profile"


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


summoner_1 = Summoner()


kv = Builder.load_file("leaguelookup.kv")


class leaguelookupApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    leaguelookupApp().run()
