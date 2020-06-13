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


class HomeGui(Widget):
    summonerName = ObjectProperty(None)

    def search_button(self):
        print("Searching for " + self.summonerName.text)
        self.summonerName.text = ""


class leaguelookupApp(App):
    def build(self):
        return HomeGui()


if __name__ == "__main__":
    leaguelookupApp().run()
