# Testing out the Riot Game League of Legends API
#       - Geoffroy Penny

import summoner_lookup
import kivy
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
import requests
import pandas
import os
from functools import partial
from kivy.clock import Clock
import json

# Key needed to lookup summoner information with riot's api
DevelopmentAPIKey = "RGAPI-3e90594d-5244-4f9d-83c9-ee5c52211206"

# Todo
#   Add a settings tab
#       choose default region
#       reorder favorites
#       color scheme
#   Profiles GUI
#   Don't rewrite all data to summoner 1 until you need it in the next class, only rewrite json
#   Add rank to the summoner name button
#   CRASH : when searching a summoner without a rank, need to add an if case to summoner_1.set_ranked_data
#   Fix transition directions
#   Challenger rank not needed: Challenger I
#   Add three buttons in profile view one for flex one for solo one for champions

# ==========================================================================================
#       Home Screen: Contains summoner lookup, region selection, and favorites
# ==========================================================================================
class HomeGui(Screen):

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

    def on_enter(self, *args):
        """
        on_enter: is overrode and used to populate and refresh the favorites and history grid when entering the screen
        :param args:
        :return:
        """
        Clock.schedule_once(lambda *args: self.populate_history())
        Clock.schedule_once(lambda *args: self.populate_favorites())

    def summoner_search(self):
        """
         summoner_search
         Checks to see if a user with the name entered exists in the region selected and brings you to their profile
            otherwise calls the correct error popup
         Adds all basic summoner data to the summoner_1 object for later use in the ProfileGui class
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
        # No summoner name entered creates popup
        elif self.summoner_name.text == "":
            popup = InvalidSearchPopup()
            popup.open_popup_2()
            print("change sum name")
        #  There is data in both entries, now we test if the summoner exists
        else:
            region = region_conversion[self.region_selection.text]
            # URL to lookup a summoners basic data
            url = "https://" + region + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + \
                  self.summoner_name.text + "?api_key=" + DevelopmentAPIKey
            url_data = requests.get(url)
            summoner_data = url_data.json()
            summoner_1.summoner_data = summoner_data

            code = url_data.status_code
            # Checks to see if the enter summoner name is valid in that region
            if code == 200:
                summoner_1.region = region
                summoner_1.set_summoner_data()
                summoner_1.set_ranked_data()

                # todo test print
                summoner_1.print_all()

                self.summoner_name.text = ""
                self.add_history()
                self.parent.current = "profile"
            # API Key out of data
            elif code == 403:
                popup = InvalidSearchPopup()
                popup.open_popup_4()
                print("API Key Outdated")
            # Gives the invalid search popup
            else:
                popup = InvalidSearchPopup()
                popup.open_popup_3()
                print(code)
                print("no summoner " + self.summoner_name.text + " found in region: " + region)

    def history_search(self, button):
        """
        history_search: searches a summoner from history bring you to their profile page
            otherwise calls the correct error popup
        Adds all basic summoner data to the summoner_1 object for later use in the ProfileGui class
        :return:
        """

        name, region = button.text.split("  :  ")
        print(" i did it bitcch ", name, region)
        # URL to lookup a summoners basic data
        url = "https://" + region + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + \
              name + "?api_key=" + DevelopmentAPIKey
        url_data = requests.get(url)
        summoner_data = url_data.json()
        summoner_1.summoner_data = summoner_data

        code = url_data.status_code

        # API Key out of data
        if code == 403:
            popup = InvalidSearchPopup()
            popup.open_popup_4()
            print("API Key Outdated")
        else:
            # All data for summoner lookup
            summoner_1.region = region
            summoner_1.set_summoner_data()
            summoner_1.set_ranked_data()

            #todo test print
            summoner_1.print_all()

            self.add_history()
            self.parent.current = "profile"


    def add_favorite(self, name, region):
        """
        add_favorite: adds a valid summoner name + region to the favorites list
        :return:
        """
        new_entry = pandas.DataFrame({'name': [name],
                                      'region': [region]})
        # If there is no favorites file, create one
        if not os.path.isfile('favorites.csv'):
            new_entry.to_csv('favorites.csv', header=['name', 'region'], index=False)
        # Else, adds name and region and deletes duplicates
        else:
            # In order to keep most recent search on top, and delete duplicates:
            #   We reverse the csv file, append the new search to the "bottom" that then becomes the top
            #   after reversing again. The we can delete all duplicates keeping the newest one making it easy to read
            #   and add to the GUI later
            df = pandas.read_csv('favorites.csv').append(new_entry).drop_duplicates(['name', 'region'])
            df.to_csv('favorites.csv', index=False)
        self.populate_favorites()

    def remove_favorites(self, button):
        """
        remove_favorite: removes the summoner name from the favorites
        :return:
        """
        index = button.id
        df = pandas.read_csv('favorites.csv')

        # Removes name from history
        df.drop(int(index)).to_csv('favorites.csv', index=False)

        self.populate_favorites()

    def populate_favorites(self):
        """
        populate_favorites: Populates the favorites grid layout with all entries in favorites.csv
        :return:
        """
        self.favorites_grid_layout.clear_widgets()
        print("POPULATING")
        if not os.path.isfile('favorites.csv'):
            new_entry = pandas.DataFrame({'name': ['HexRoy'],
                                          'region': ['NA1']})
            new_entry.to_csv('favorites.csv', header=['name', 'region'], index=False)

        df = pandas.read_csv('favorites.csv')
        for index, line in df.iterrows():
            summoner_button = Button(text=line['name'] + "  :  " + line['region'], size_hint=(None, None),
                                     height=self.height / 10, width=self.width / 3.5)
            summoner_button.bind(on_press=partial(self.history_search))

            favorite_button = Button(background_normal="images/goldstar.png", background_down="images/blackstar.png",
                                     size_hint=(None, None), height=self.height / 10, width=self.width / 10,
                                     id=str(index))
            favorite_button.bind(on_press=partial(self.remove_favorites))

            self.favorites_grid_layout.add_widget(summoner_button)
            self.favorites_grid_layout.add_widget(favorite_button)

    @staticmethod
    def add_history():
        """
        add_history: add a successful summoner search to the history.csv file
        :return:
        """
        new_entry = pandas.DataFrame({'name': [summoner_1.name],
                                      'region': [summoner_1.region]})
        # If there is no history file, create one
        if not os.path.isfile('history.csv'):
            new_entry.to_csv('history.csv', header=['name', 'region'], index=False)
        # Else, adds new search and deletes duplicates
        else:
            # In order to keep most recent search on top, and delete duplicates:
            #   We reverse the csv file, append the new search to the "bottom" that then becomes the top
            #   after reversing again. The we can delete all duplicates keeping the newest one making it easy to read
            #   and add to the GUI later
            df = pandas.read_csv('history.csv').iloc[::-1].append(new_entry)
            df.iloc[::-1].drop_duplicates(['name', 'region']).to_csv('history.csv', index=False)

    def remove_history(self, button):
        """
        remove_history: Removes the summoner name from the history by index
                        Calls populate_history to update grid layout
                        Calls add_favorites to add it to the favorites grid layout
        :return:
        """
        index = button.id
        df = pandas.read_csv('history.csv')

        # Gets name and region to be added to favorites before its removed from history
        name = df.iloc[int(index)]['name']
        region = df.iloc[int(index)]['region']

        # Removes name from history
        df.drop(int(index)).to_csv('history.csv', index=False)

        self.populate_history()
        self.add_favorite(name, region)

    def populate_history(self):
        """
        populate_history: Populates the history grid layout with all entries in history.csv
        :return:
        """

        self.history_grid_layout.clear_widgets()

        if not os.path.isfile('history.csv'):
            new_entry = pandas.DataFrame({'name': ['HexRoy'],
                                          'region': ['NA1']})
            new_entry.to_csv('history.csv', header=['name', 'region'], index=False)

        df = pandas.read_csv('history.csv')
        for index, line in df.iterrows():
            summoner_button = Button(text=line['name']+"  :  "+line['region'], size_hint=(None, None), height=self.height/10, width=self.width/3.5)
            summoner_button.bind(on_press=partial(self.history_search))

            favorite_button = Button(background_normal="images/blackstar.png", background_down="images/goldstar.png", size_hint=(None, None), height=self.height/10, width=self.width/10, id=str(index))
            favorite_button.bind(on_press=partial(self.remove_history))

            self.history_grid_layout.add_widget(summoner_button)
            self.history_grid_layout.add_widget(favorite_button)


# ==========================================================================================
#       Invalid Search Popup: Displays popups for bad searches
#           Types:  1 = No region selected
#                   2 = No summoner name input
#                   3 = Bad search: the combination is not found
#                   4 = API Key is outdated
# ==========================================================================================
class InvalidSearchPopup(FloatLayout):
    # Variables pulled from from <HomeGui> leaguelookup.kv
    popup_label = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(FloatLayout, self).__init__(**kwargs)
        self.popup = Popup(title="Error!", content=self, size_hint=(.3, .3), auto_dismiss=True)

    def open_popup_1(self):
        """
        open_popup_1: opens the no region selected popup
        :return:
        """
        self.popup_label.text = "Select a region"
        self.popup.open()

    def open_popup_2(self):
        """
        open_popup_2: opens the no summoner name popup
        :return:
        """
        self.popup_label.text = "Enter a summoner name"
        self.popup.open()

    def open_popup_3(self):
        """
        open_popup_3: opens the summoner not found popup
        :return:
        """
        self.popup_label.text = "Summoner not found"
        self.popup.open()

    def open_popup_4(self):
        """
        open_popup_4: opens the api key outdated popup
        :return:
        """
        self.popup_label.text = "API Key Outdated"
        self.popup.open()

    def close_popup(self):
        """
        close_popup: closes any of the three popups
        :return:
        """
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

    def on_enter(self):
        """
        on_enter: Determines what happens upon entering the screen "Profile"
        :return:
        """
        self.profile_summoner_name.text = summoner_1.name

        self.profile_solo_rank_icon.source = 'images/ranks/Emblem_' + summoner_1.solo_tier + '.png'
        solo_rank = summoner_1.solo_tier + " " + summoner_1.solo_rank + " " + str(summoner_1.solo_league_points) + " LP"
        self.profile_solo_rank.text = solo_rank
        self.profile_solo_win_loss.text = 'W/L: ' + str(summoner_1.solo_wins) + "/" + str(summoner_1.solo_losses)

        self.profile_flex_rank_icon.source = 'images/ranks/Emblem_' + summoner_1.flex_tier+ '.png'
        flex_rank = summoner_1.flex_tier + " " + summoner_1.flex_rank + " " + str(summoner_1.flex_league_points) + " LP"
        self.profile_flex_rank.text = flex_rank
        self.profile_flex_win_loss.text = 'W/L: ' + str(summoner_1.flex_wins) + "/" + str(summoner_1.flex_losses)

        self.populate_match_history()

    def populate_match_history(self):
        """
        populate_match_history: populates the match history grid, with most recent 20 games
        :return:
        """
        self.profile_match_history.clear_widgets()

        url = "https://" + summoner_1.region + ".api.riotgames.com/lol/match/v4/matchlists/by-account/"+ summoner_1.account_id +"?endIndex=20&api_key=" + DevelopmentAPIKey
        match_history = requests.get(url)
        match_history = match_history.json()

        for match in match_history['matches']:
            view_button = Button(text="View Match", size_hint=(None, None), height=self.height/8, width=self.width/9, id=str(match['gameId']))
            view_button.bind(on_press=partial(self.match_search))
            self.profile_match_history.add_widget(view_button)

            # Gets the champions that is played in the game
            with open('data_dragon_10.14.1/10.14.1/data/en_US/champion.json', 'r', encoding="utf-8") as champion_data:
                champion_dict = json.load(champion_data)

            for champion in champion_dict['data']:
                try:
                    test = list(champion_dict['data'][champion].keys())[list(champion_dict['data'][champion].values()).index(str(match['champion']))]
                    break
                except ValueError:
                    pass

            champion_image = Image(source='data_dragon_10.14.1/10.14.1/img/champion/'+champion+'.png', size_hint=(None, None), height=self.height/8)
            self.profile_match_history.add_widget(champion_image)

            # Obtains the matches data
            url = 'https://' + summoner_1.region + '.api.riotgames.com/lol/match/v4/matches/' + str(match['gameId']) +'?api_key=' + DevelopmentAPIKey
            match_data = requests.get(url)
            match_data = match_data.json()

            # To get game length --> minutes:seconds
            match_length = match_data['gameDuration']/60
            minutes = int(match_length)
            seconds = (match_length*60) % 60
            time = ("%d:%02d" % (minutes, seconds))

            for players in match_data['participants']:
                if players['championId'] == match['champion']:

                    print(players['stats'])

                    # TODO convert ids to name/get icon --> datadragon summoner
                    spell_1 = players['spell1Id']
                    spell_2 = players['spell2Id']
                    keystone_primary = None
                    keystone_secondary = None
                    rune_1 = None
                    rune_2 = None
                    rune_3 = None

                    win = players['stats']['win']

                    kills = players['stats']['kills']
                    deaths = players['stats']['deaths']
                    assists = players['stats']['assists']
                    kda = ("%d/%d/%d" % (kills, deaths, assists))
                    kda_label = Label(text=kda, size_hint=(None, None), height=self.height/8)
                    self.profile_match_history.add_widget(kda_label)

                    item_grid_layout = GridLayout(cols=3, spacing=0)
                    for i in range(6):
                        item = players['stats']['item%d' % i]
                        if item == 0:
                            pass
                        else:
                            item_image = Image(source='data_dragon_10.14.1/10.14.1/img/item/' + str(item) + ".png", size_hint=(None, None), width=self.width/14, height=self.height/16)
                            item_grid_layout.add_widget(item_image)
                    self.profile_match_history.add_widget(item_grid_layout)
                    break




    def match_search(self, button):
        self.parent.current = "match"


# ==========================================================================================
#       Match Gui: Statistics about a specific game
# ==========================================================================================
class MatchGui(Screen):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.name = 'match'


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
        self.region = None              # The summoners region
        self.summoner_data = None       # JSON of all summoners data - obtained from requests()
        self.account_id = None
        self.puuid = None
        self.id = None
        self.name = None
        self.profile_icon_id = None
        self.revision_date = None
        self.summoner_level = None

        self.ranked_data = None
        self.solo_tier = None
        self.solo_rank = None
        self.solo_league_points = None
        self.solo_wins = None
        self.solo_losses = None
        self.solo_veteran = None
        self.solo_inactive = None
        self.solo_fresh_blood = None
        self.solo_hot_streak = None
        self.flex_tier = None
        self.flex_rank = None
        self.flex_league_points = None
        self.flex_wins = None
        self.flex_losses = None
        self.flex_veteran = None
        self.flex_inactive = None
        self.flex_fresh_blood = None
        self.flex_hot_streak = None

    def set_summoner_data(self):
        summoner_1.name = summoner_1.summoner_data['name']
        summoner_1.account_id = summoner_1.summoner_data['accountId']
        summoner_1.puuid = summoner_1.summoner_data['puuid']
        summoner_1.id = summoner_1.summoner_data['id']
        summoner_1.profile_icon_id = summoner_1.summoner_data['profileIconId']
        summoner_1.revision_date = summoner_1.summoner_data['revisionDate']
        summoner_1.summoner_level = summoner_1.summoner_data['summonerLevel']

    def set_ranked_data(self):
        url = 'https://' + summoner_1.region + '.api.riotgames.com/lol/league/v4/entries/by-summoner/' \
              + summoner_1.id + '?api_key=' + DevelopmentAPIKey
        data = requests.get(url)
        self.ranked_data = data.json()

        # Sometimes the league api json for ranked data swaps the order of solo rank and flex rank
        # This makes sure the correct rank is assigned to solo and flex
        if self.name == "WeBrewin":
            self.solo_tier = 'Challenger'
            self.solo_rank = ''
            self.solo_league_points = '900'
            self.flex_tier = 'Diamond'
            self.flex_rank = 'I'
            self.flex_league_points = 90
        else:
            for i in range(len(self.ranked_data)):
                if self.ranked_data[i]['queueType'] == 'RANKED_SOLO_5x5':
                    self.solo_tier = self.ranked_data[i]['tier']
                    self.solo_rank = self.ranked_data[i]['rank']
                    self.solo_league_points = self.ranked_data[i]['leaguePoints']
                    self.solo_wins = self.ranked_data[i]['wins']
                    self.solo_losses = self.ranked_data[i]['losses']
                    self.solo_veteran = self.ranked_data[i]['veteran']
                    self.solo_inactive = self.ranked_data[i]['inactive']
                    self.solo_fresh_blood = self.ranked_data[i]['freshBlood']
                    self.solo_hot_streak = self.ranked_data[i]['hotStreak']

                else:
                    self.flex_tier = self.ranked_data[i]['tier']
                    self.flex_rank = self.ranked_data[i]['rank']
                    self.flex_league_points = self.ranked_data[i]['leaguePoints']
                    self.flex_wins = self.ranked_data[i]['wins']
                    self.flex_losses = self.ranked_data[i]['losses']
                    self.flex_veteran = self.ranked_data[i]['veteran']
                    self.flex_inactive = self.ranked_data[i]['inactive']
                    self.flex_fresh_blood = self.ranked_data[i]['freshBlood']
                    self.flex_hot_streak = self.ranked_data[i]['hotStreak']

    def print_all(self):
        print("region", self.region)
        print("summoner_data", self.summoner_data)
        print("account_id", self.account_id)
        print("puuid", self.puuid)
        print("id", self.id)
        print("name", self.name)
        print("profile_icon_id", self.profile_icon_id)
        print("revision_date", self.revision_date)
        print("summoner_level", self.summoner_level)

        print("ranked data", self.ranked_data)
        print("solo_tier", self.solo_tier)
        print("solo_rank", self.solo_rank)
        print("solo_league_points", self.solo_league_points)
        print("solo_wins", self.solo_wins)
        print("solo_losses", self.solo_losses)
        print("solo_veteran", self.solo_veteran)
        print("solo_inactive", self.solo_inactive)
        print("solo_fresh_blood", self.solo_fresh_blood)
        print("solo_hot_streak", self.solo_hot_streak)
        print("flex_tier", self.flex_tier)
        print("flex_rank", self.flex_rank)
        print("flex_league_points", self.flex_league_points)
        print("flex_wins", self.flex_wins)
        print("flex_losses", self.flex_losses)
        print("flex_veteran", self.flex_veteran)
        print("flex_inactive", self.flex_inactive)
        print("flex_fresh_blood", self.flex_fresh_blood)
        print("flex_hot_streak", self.flex_hot_streak)


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
