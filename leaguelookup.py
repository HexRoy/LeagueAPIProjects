# Testing out the Riot Game League of Legends API
#       - Geoffroy Penny

# Imports
#   Kivy
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
#   Other
import requests
import pandas
import os
from functools import partial
from kivy.clock import Clock
import json
import cassiopeia as cass
import pprint
from time import sleep
import datetime


# Key needed to lookup summoner information with riot's api
DevelopmentAPIKey = "RGAPI-baca05a2-f4c3-4d2c-8d04-e43aca394822"
cass.set_riot_api_key(DevelopmentAPIKey)
data_dragon_version = '11.4.1'


# Todo
#   Add a settings tab
#       choose default region
#           if default region: auto select that for drop down
#       color scheme
#       'Reset All' button: search history and favorites with confirmation popup
#   Home GUI
#       reorder favorites
#       Revamp region/setting + button text
#   Profiles GUI
#       Integrate cassiopeia
#       Don't rewrite all data to summoner 1 until you need it in the next class, only rewrite json
#       Add rank to the summoner name button
#       Add star to remove/ add to favorites
#       Add variable spacing between widgets in match history scroll view, currently set to 20
#       Add progress bar for loading matches
#       Ranked: solo
#           Add expand view to add more games, and throttling when loading to avoid timeout
#           Possibly save game previously loaded for quicker access
#       Ranked: flex
#           Add expand view to add more games, and throttling when loading to avoid timeout
#           Possibly save game previously loaded for quicker access
#   Match GUI
#       Add view summoner button next to other summoners in the game
#   Champions
#       Add filtering by season
#       Calculate KDA after saving: Save  Kills+assists | Deaths
#           When populating check for division by zero
#   Single Champion
#       win rates on one champion vs every champion you have played against
#       Calculate KDA after saving: Save  Kills+assists | Deaths
#           When populating check for division by zero
#   Live Game
#   CRASH : something to do with time duration of a match (possibly aram games have a different variable)
#       It is timing because of rate limits on league api
#   Bug: When updating new games: all previous data got erased? need to do more testing
#   Fix: transition directions for each screen
#   Challenger rank not needed: Challenger I


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
                summoner_1.cass_region = self.region_selection.text
                summoner_1.region = region
                summoner_1.set_summoner_data()
                summoner_1.set_ranked_data()
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
            # Todo: can be removed if ever fully committed tocassiopeiaa
            region_conversion = {
                "BR1": "BR",
                "EUN1": "EUN",
                "EUW1": "EUW",
                "JP1": "JP",
                "KR": "KR",
                "LA1": "LA1",
                "LA2": "LA2",
                "NA1": "NA",
                "OC1": "OC",
                "TR1": "TR",
                "RU": "RU",
                }
            summoner_1.cass_region = region_conversion[region]

            # All data for summoner lookup
            summoner_1.region = region
            summoner_1.set_summoner_data()
            summoner_1.set_ranked_data()
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
        if not os.path.isfile('favorites.csv'):
            new_entry = pandas.DataFrame({'name': ['HexRoy'],
                                          'region': ['NA1']})
            new_entry.to_csv('favorites.csv', header=['name', 'region'], index=False)

        df = pandas.read_csv('favorites.csv')
        for index, line in df.iterrows():
            summoner_button = Button(background_normal="images/button background.png", color=(0, 0, 0, 1), text=line['name'] + "  :  " + line['region'], size_hint=(None, None),
                                     height=self.height / 10, width=self.width / 3.5)
            summoner_button.bind(on_press=partial(self.history_search))

            favorite_button = Button(background_normal="images/goldstar.png", background_down="images/blackstar.png", size_hint=(None, None), height=self.height/10, width=self.width/10) #, id=str(index))
            favorite_button.id = str(index)
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
            summoner_button = Button(background_normal="images/button background2.png", text=line['name']+"  :  "+line['region'], size_hint=(None, None), height=self.height/10, width=self.width/3.5)
            summoner_button.bind(on_press=partial(self.history_search))

            favorite_button = Button(background_normal="images/blackstar.png", background_down="images/goldstar.png", size_hint=(None, None), height=self.height/10, width=self.width/10)
            favorite_button.id = str(index)
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

    def open_popup_5(self):
        """
        open_popup_5: opens the new no games played popup
        :return:
        """
        self.popup_label.text = "Up to date"
        self.popup.open()

    def close_popup(self):
        """
        close_popup: closes any of the three popups
        :return:
        """
        self.popup.dismiss()


# ==========================================================================================
#       Profile Gui: Overview of the searched summoner. Rank, win rate, match history
# ==========================================================================================
class ProfileGui(Screen):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.name = "profile"
        self.url = None

    def on_enter(self):
        """
        on_enter: Determines what happens upon entering the screen "Profile"
        If we are entering the same profile that is already loaded, do nothing
        Otherwise load the new profile
        :return:
        """
        if self.profile_summoner_name.text == summoner_1.name:
            self.url = "https://" + str(summoner_1.region) + ".api.riotgames.com/lol/match/v4/matchlists/by-account/" + str(summoner_1.account_id) + "?endIndex=2&api_key=" + str(DevelopmentAPIKey)
        else:
            self.url = "https://" + str(summoner_1.region) + ".api.riotgames.com/lol/match/v4/matchlists/by-account/" + str(summoner_1.account_id) + "?endIndex=2&api_key=" + str(DevelopmentAPIKey)

            # Summoner name and level
            self.profile_summoner_name.text = summoner_1.name
            self.profile_summoner_level.text = 'Level: ' + str(summoner_1.summoner_level)

            # For solo queue
            if summoner_1.solo_rank is not None:
                self.profile_solo_rank_icon.source = 'images/ranks/Emblem_' + summoner_1.solo_tier + '.png'
                solo_rank = summoner_1.solo_tier + " " + summoner_1.solo_rank + " " + str(summoner_1.solo_league_points) + " LP"
                self.profile_solo_rank.text = solo_rank
                self.profile_solo_win_loss.text = 'W/L: ' + str(summoner_1.solo_wins) + "/" + str(summoner_1.solo_losses)
            else:
                self.profile_solo_rank_icon.source = 'images/ranks/Emblem_Unranked.png'
                self.profile_solo_rank.text = "Unranked"
                self.profile_solo_win_loss.text = 'W/L: Not Available'

            # For flex queue
            if summoner_1.flex_rank is not None:
                self.profile_flex_rank_icon.source = 'images/ranks/Emblem_' + summoner_1.flex_tier + '.png'
                flex_rank = summoner_1.flex_tier + " " + summoner_1.flex_rank + " " + str(summoner_1.flex_league_points) + " LP"
                self.profile_flex_rank.text = flex_rank
                self.profile_flex_win_loss.text = 'W/L: ' + str(summoner_1.flex_wins) + "/" + str(summoner_1.flex_losses)
            else:
                self.profile_flex_rank_icon.source = 'images/ranks/Emblem_Unranked.png'
                self.profile_flex_rank.text = "Unranked"
                self.profile_flex_win_loss.text = 'W/L: Not Available'

            self.populate_match_history()

    def populate_match_history(self):
        """
        populate_match_history: populates the match history grid, with most recent 20 games
        :return:
        """
        self.profile_match_history.clear_widgets()
        match_history = requests.get(self.url)
        match_history = match_history.json()

        # Creates a champion id to name conversion dictionary
        with open('data_dragon_' + data_dragon_version + '/' + data_dragon_version + '/data/en_US/champion.json', 'r', encoding="utf-8") as champion_data:
            champion_dict = json.load(champion_data)
        champion_id_to_name = {}
        for key in champion_dict['data']:
            row = champion_dict['data'][key]
            champion_id_to_name[row['key']] = row['id']

        for match in match_history['matches']:
            # View match button
            view_button = Button(text="View Match", size_hint=(None, None), height=self.height/8, width=self.width/9)
            view_button.id = str(match['gameId'])
            view_button.bind(on_press=partial(self.match_search))
            self.profile_match_history.add_widget(view_button)

            # The champion image
            champion_name = champion_id_to_name.get(str(match['champion']))

            if champion_name is not None:
                champion_image = Image(source='data_dragon_' + data_dragon_version + '/' + data_dragon_version + '/img/champion/' + champion_name + '.png', size_hint=(None, None), height=self.height/8)
                self.profile_match_history.add_widget(champion_image)
            else:
                self.profile_match_history.add_widget(Image(source='data_dragon_' + data_dragon_version + '/' + data_dragon_version + '/img/champion/None.png', size_hint=(None, None), height=self.height/8))

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

                    # TODO convert ids to name/get icon --> datadragon summoner
                    spell_1_id = players['spell1Id']
                    spell_2_id = players['spell2Id']
                    keystone_primary = None
                    keystone_secondary = None
                    rune_1 = None
                    rune_2 = None
                    rune_3 = None
                    win = players['stats']['win']
                    largest_multikill = players['stats']['largestMultiKill']
                    largest_killingspree = players['stats']['largestKillingSpree']
                    kills = players['stats']['kills']
                    deaths = players['stats']['deaths']
                    assists = players['stats']['assists']
                    champion_level = players['stats']['champLevel']
                    kda = ("%d/%d/%d" % (kills, deaths, assists))
                    if deaths == 0:
                        calculated_kda = "Infinite"
                    else:
                        calculated_kda = round(((kills + assists) / deaths), 2)
                    cs = players['stats']['totalMinionsKilled'] + players['stats']['neutralMinionsKilled']
                    cs_per_minute = round(cs/minutes, 1)

                    kda_label = Label(text="Level: " + str(champion_level) + "\n" + kda + "\nKDA: " + str(calculated_kda) + "\nCS: " + str(cs) + " (" + str(cs_per_minute) + ")", size_hint=(None, None), height=self.height/8)
                    self.profile_match_history.add_widget(kda_label)

                    item_grid_layout = GridLayout(cols=3)
                    for i in range(6):
                        item = players['stats']['item%d' % i]
                        if item == 0:
                            pass
                        else:
                            item_image = Image(source='data_dragon_' + data_dragon_version + '/' + data_dragon_version + '/img/item/' + str(item) + ".png",allow_stretch=True, keep_ratio=False, size_hint=(None, None), width=self.width/14, height=self.height/17)
                            item_grid_layout.add_widget(item_image)
                    self.profile_match_history.add_widget(item_grid_layout)

                    # Opens the summoner spells json file
                    with open('data_dragon_' + data_dragon_version + '/' + data_dragon_version + '/data/en_US/summoner.json', 'r', encoding="utf-8") as summoner_spells:
                        spell_dict = json.load(summoner_spells)

                    # Finds spell 1
                    for spell1 in spell_dict['data']:
                        try:
                            test = list(spell_dict['data'][spell1].keys())[list(spell_dict['data'][spell1].values()).index(str(spell_1_id))]
                            break
                        except ValueError:
                            pass
                    # Finds spell 2
                    for spell2 in spell_dict['data']:
                        try:
                            test = list(spell_dict['data'][spell2].keys())[list(spell_dict['data'][spell2].values()).index(str(spell_2_id))]
                            break
                        except ValueError:
                            pass
                    spell_1_name = spell1
                    spell_2_name = spell2

                    # Adds spells and ward icon to match history
                    spell_grid_layout = GridLayout(cols=3, spacing=(.1, 0))
                    ward_image = Image(source='data_dragon_' + data_dragon_version + '/' + data_dragon_version + '/img/item/' + str(players['stats']['item6']) + ".png",  keep_ratio=False, size_hint=(None, None), width=self.width / 14, height=self.height / 17)
                    spell1_image = Image(source='data_dragon_' + data_dragon_version + '/' + data_dragon_version + '/img/spell/' + spell_1_name + ".png", allow_stretch=True, keep_ratio=False, size_hint=(None, None), width=self.width / 14, height=self.height / 17)
                    spell2_image = Image(source='data_dragon_' + data_dragon_version + '/' + data_dragon_version + '/img/spell/' + spell_2_name + ".png", allow_stretch=True, keep_ratio=False, size_hint=(None, None), width=self.width / 14, height=self.height / 17)
                    spell_grid_layout.add_widget(ward_image)
                    spell_grid_layout.add_widget(spell1_image)
                    spell_grid_layout.add_widget(spell2_image)
                    self.profile_match_history.add_widget(spell_grid_layout)

                    time_label = Label(text=str(time))
                    self.profile_match_history.add_widget(time_label)
                    break

    def match_search(self, button):
        """
        match_search: used the match id added to the view button on creation to get more detailed match information
        :param button: "view match" button
        :return:
        """
        summoner_1.current_match_id = button.id
        self.parent.current = "match"

    def set_ranked_solo(self):
        """
        set_ranked_solo: sets the url to filter by solo ranked games
        :return:
        """
        self.url = "https://" + summoner_1.region + ".api.riotgames.com/lol/match/v4/matchlists/by-account/" + summoner_1.account_id + "?queue=420&endIndex=2&api_key=" + str(DevelopmentAPIKey)
        self.populate_match_history()

    def set_ranked_flex(self):
        """
        set_ranked_flex: sets the url to filter by flex ranked games
        :return:
        """
        self.url = "https://" + summoner_1.region + ".api.riotgames.com/lol/match/v4/matchlists/by-account/" + summoner_1.account_id + "?queue=440&endIndex=2&api_key=" + str(DevelopmentAPIKey)
        self.populate_match_history()

    def set_ranked_clash(self):
        """
        set_ranked_clash: sets the url to filter by clash games
        :return:
        """
        self.url = "https://" + summoner_1.region + ".api.riotgames.com/lol/match/v4/matchlists/by-account/" + summoner_1.account_id + "?queue=700&endIndex=2&api_key=" + str(DevelopmentAPIKey)
        self.populate_match_history()

    def set_all_games(self):
        """
        set_all_games: sets the url to filter by all gamess
        :return:
        """
        self.url = "https://" + str(summoner_1.region) + ".api.riotgames.com/lol/match/v4/matchlists/by-account/" + str(summoner_1.account_id) + "?endIndex=2&api_key=" + str(DevelopmentAPIKey)
        self.populate_match_history()


# ==========================================================================================
#       Match Gui: Statistics about a specific game
# ==========================================================================================
class MatchGui(Screen):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.name = 'match'
        self.match_data = None

    def on_enter(self, *args):
        """
        on_enter: Determines what happens when entering the MatchGUI page
        :param args:
        :return:
        """

        #TODO Posible remove
        # Obtains the matches data
        url = 'https://' + summoner_1.region + '.api.riotgames.com/lol/match/v4/matches/' + str(
            summoner_1.current_match_id) + '?api_key=' + DevelopmentAPIKey
        match_data = requests.get(url)
        match_data = match_data.json()
        self.match_data = match_data

        self.populate_match_data()

    def populate_match_data(self):
        """
        populate_match_data: adds all of the match data to the grid layout
        :return:
        """
        self.match_grid_layout.clear_widgets()

        match = cass.get_match(int(summoner_1.current_match_id), summoner_1.cass_region)
        red_team = match.red_team.to_dict()
        blue_team = match.blue_team.to_dict()

        self.team_loop(red_team)
        self.team_loop(blue_team)

    def team_loop(self, team_data):
        """
        team_loop: loops through one of the teams to populate the match grid layout
        :param team_data: a dict containing all of the teams data
        :return:
        """

        if team_data['isWinner']:
            text_color = '11d111'   # Green
        else:
            text_color = 'ff3333'   # Red

        for summoner in team_data['participants']:
            name = summoner['summonerName']
            champion_id = summoner['championId']

            # Creates a champion id to name conversion dictionary
            with open('data_dragon_' + data_dragon_version + '/' + data_dragon_version + '/data/en_US/champion.json', 'r', encoding="utf-8") as champion_data:
                champion_dict = json.load(champion_data)

            champion_id_to_name = {}
            for key in champion_dict['data']:
                row = champion_dict['data'][key]
                champion_id_to_name[row['key']] = row['id']

            champion_name = champion_id_to_name.get(str(champion_id))
            if champion_name is not None:
                champion_image = Image(source='data_dragon_' + data_dragon_version + '/' + data_dragon_version + '/img/champion/' + champion_name + '.png', size_hint=(None, None), height=self.height / 8, width=self.width/10)
            else:
                champion_image = Image(source='data_dragon_1' + data_dragon_version + '/' + data_dragon_version + '/img/champion/None.png', size_hint=(None, None), height=self.height / 8, width=self.width / 10)

            #TODO REmove
            pprint.pprint(summoner)
            print("========================================================================================================================================================================")

            level = summoner['stats']['champLevel']

            # Obtains KDA Information
            KDA = ("%d/%d/%d" % (summoner['stats']['kills'], summoner['stats']['deaths'], summoner['stats']['assists']))
            if summoner['stats']['deaths'] == 0:
                calculated_kda = "Infinite"
            else:
                calculated_kda = round(
                    ((summoner['stats']['kills'] + summoner['stats']['assists']) / summoner['stats']['deaths']), 2)

            # To get game length --> minutes:seconds
            match_length = self.match_data['gameDuration'] / 60
            minutes = int(match_length)

            cs = summoner['stats']['neutralMinionsKilled'] + summoner['stats']['totalMinionsKilled']
            cs_per_minute = round(cs / minutes, 1)

            stats = 'Level: ' + str(level) + '\n' + KDA + '\nKDA: ' + str(calculated_kda) + '\nCS: ' + str(cs) + " (" + str(cs_per_minute) + ")"



            damage = summoner['stats']['totalDamageDealtToChampions']
            wards = ('Normal: %d\nKilled: %d\nPinks: %d' %(summoner['stats']['wardsPlaced'], summoner['stats']['wardsKilled'], summoner['stats']['visionWardsBoughtInGame']))

            items = [summoner['stats']['item0'], summoner['stats']['item1'], summoner['stats']['item2'], summoner['stats']['item3'], summoner['stats']['item4'], summoner['stats']['item5']]
            objectives = "None"
            towers = "None"

            # Adds/Creates all labels for the grid layout
            self.create_label(name)
            self.match_grid_layout.add_widget(champion_image)
            self.create_label(stats)
            self.add_item_images(items)
            self.create_label(damage)
            self.create_label(wards)
            self.create_label(objectives)
            self.create_label(towers)

    def add_item_images(self, item_list):
        """
        add_item_images: Takes an item id list and creates a grid layout of item images
        :param item_list: list of int's representing item id's
        :return:
        """
        item_grid_layout = GridLayout(cols=3)
        for item in item_list:
            if item == 0:
                pass
            else:
                item_image = Image(source='data_dragon_' + data_dragon_version + '/' + data_dragon_version + '/img/item/' + str(item) + ".png",
                                   allow_stretch=True, keep_ratio=False, size_hint=(None, None),
                                   width=self.width / 14, height=self.height / 17)
                item_grid_layout.add_widget(item_image)
        self.match_grid_layout.add_widget(item_grid_layout)

    def create_label(self, label_text):
        """
        create_label: creates and adds label to the grid layout with specified text
        :param label_text: a string of text that will be the label
        :return:
        """
        label = Label(text=str(label_text), size_hint=(None, None), height=self.height / 8, width=self.width/10)
        self.match_grid_layout.add_widget(label)


# ==========================================================================================
#       Settings Gui: Contains the user settings for the app
# ==========================================================================================
class SettingsGui(Screen):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)


# ==========================================================================================
#       All Champions Gui: List of all champion stats from the current season
# ==========================================================================================
class AllChampionsGui(Screen):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.account_url = None
        self.match_url = None
        self.win_rates = {}
        self.all_kda = {}
        self.champ_sort = False
        self.win_rate_sort = False
        self.no_new_data = False

        # Beginning of season 11 - Epoch millisecond
        self.last_update = 1610118000000

    def on_enter(self, *args):
        """
        on_enter: Determines what happens when entering the AllChampionsGui page
        :param args:
        :return:
        """
        # Clears win rates dictionary and previous loads
        self.all_champions_grid_layout.clear_widgets()

        summoners_path = 'winrate_csv/' + summoner_1.name

        # If no directory is found for the summoner, creates one
        if not os.path.isdir(summoners_path):
            os.mkdir(summoners_path)

        # If data is not found for the summoner
        if not os.path.isfile(summoners_path + '/all_champions_win_rates.csv'):

            self.calculate_win_rates()
            self.save_win_rates()

        self.populate_all_champion_win_rates()

    def calculate_win_rates(self):
        """
        calculate_win_rates - To calculate and update your champion win rates
        :return:
        """

        # Clears any previous temp data
        self.win_rates = {}
        self.all_kda = {}

        # If there is saved data
        if os.path.isfile('winrate_csv/' + summoner_1.name + '/all_champions_win_rates.csv'):
            df = pandas.read_csv('winrate_csv/' + summoner_1.name + '/all_champions_win_rates.csv')
            for index, line in df.iterrows():

                if not pandas.isna(line['champion_name']):
                    champion_name = 'None'
                else:
                    champion_name = line['champion_name']
                wins = line['wins']
                losses = line['losses']
                self.win_rates[champion_name] = [wins, losses]

        self.account_url = "https://" + summoner_1.region + ".api.riotgames.com/lol/match/v4/matchlists/by-account/" + summoner_1.account_id + "?queue=420&beginTime=" + str(self.last_update) + "&api_key=" + str(DevelopmentAPIKey)

        account_details = requests.get(self.account_url)

        # Checking for 404 error: no new data
        status = account_details.status_code

        if status != 404:
            account_details = account_details.json()
            total_games = account_details['totalGames']
            begin_index = 0

            # Creates a champion id to name conversion dictionary
            with open('data_dragon_' + data_dragon_version + '/' + data_dragon_version + '/data/en_US/champion.json', 'r',
                      encoding="utf-8") as champion_data:
                champion_dict = json.load(champion_data)
            champion_id_to_name = {}
            for key in champion_dict['data']:
                row = champion_dict['data'][key]
                champion_id_to_name[row['key']] = row['id']

            # Loops through the sets of 100 games
            while begin_index < total_games:
                self.match_url = 'https://' + summoner_1.region + '.api.riotgames.com/lol/match/v4/matchlists/by-account/' + summoner_1.account_id + '?queue=420&beginTime=' + str(self.last_update) + '&beginIndex=' + str(begin_index) + '&api_key=' + str(DevelopmentAPIKey)
                match_history = requests.get(self.match_url)
                match_history = match_history.json()
                matches = match_history['matches']

                # Loops through all matches in match_data
                for match in matches:

                    # Todo Using sleep to delay the calls to riot api
                    sleep(2)
                    print('sleeping 2 seconds')

                    current_champ = match['champion']
                    current_champion_name = champion_id_to_name.get(str(current_champ))

                    game_id = str(match['gameId'])

                    match_lookup = 'https://' + summoner_1.region + '.api.riotgames.com/lol/match/v4/matches/' + game_id + '?api_key=' + str(DevelopmentAPIKey)
                    match_lookup = requests.get(match_lookup)
                    match_lookup = match_lookup.json()

                    # Loops through each player in the match
                    for summoner in match_lookup['participants']:
                        if summoner['championId'] == current_champ:

                            # Calculates the winrates for each champion
                            win = summoner['stats']['win']

                            if current_champion_name in self.win_rates:
                                if win is True:
                                    self.win_rates[current_champion_name][0] = self.win_rates[current_champion_name][0]+1
                                else:
                                    self.win_rates[current_champion_name][1] = self.win_rates[current_champion_name][1]+1
                            else:
                                if win is True:
                                    self.win_rates[current_champion_name] = [1, 0]
                                else:
                                    self.win_rates[current_champion_name] = [0, 1]

                            # Calculates the kda for each champion
                            kills = summoner['stats']['kills']
                            deaths = summoner['stats']['deaths']
                            assists = summoner['stats']['assists']
                            kills_assists = kills + assists

                            if current_champion_name in self.all_kda:
                                self.all_kda[current_champion_name][0] = self.all_kda[current_champion_name][0] + kills_assists
                                self.all_kda[current_champion_name][1] = self.all_kda[current_champion_name][1] + deaths
                            else:
                                self.all_kda[current_champion_name] = [kills_assists, deaths]

                    print('loaded 1 game')

                # Maximum number of games that can be loaded at once is 100
                begin_index += 100

        else:
            self.no_new_data = True

    def populate_all_champion_win_rates(self):
        """
        populate_all_champion_win_rates: Adds champion data to the grid layout
        :return:
        """

        df = pandas.read_csv('winrate_csv/' + summoner_1.name + '/all_champions_win_rates.csv')
        for index, line in df.iterrows():

            # Champion Name + Icon
            champion_name = line['champion_name']
            if not pandas.isna(line['champion_name']):
                champion_image = Image(source='data_dragon_' + data_dragon_version + '/' + data_dragon_version + '/img/champion/' + champion_name + '.png',
                                       size_hint=(None, None), height=self.height / 8)
            else:
                champion_image = Image(source='data_dragon_' + data_dragon_version + '/' + data_dragon_version + '/img/champion/None.png', size_hint=(None, None), height=self.height / 8)
            champion_name_label = Label(text=str(champion_name), size_hint=(None, None), height=self.height/8)

            # Converts the string representation of the win rate list list, to a list
            win_rate = line['win_rates']
            wins = line['wins']
            losses = line['losses']
            kills_assists = line['kills_assists']
            deaths = line['deaths']

            if deaths == 0:
                kda = 'Infinite'
            else:
                kda = round((kills_assists / deaths), 2)

            calculated_kda_text = 'KDA: ' + str(kda)
            calculated_win_rate_text = str(win_rate) + ' % : (' + str(wins) + ' / ' + str(losses) + ')'

            if win_rate <= 25:
                color = [1, 0, 0, 1]
            elif 25 <= win_rate <= 45:
                color = [1, .5, 0, 1]
            elif 45 <= win_rate <= 50:
                color = [1, 1, 0, 1]
            elif 50 <= win_rate <= 55:
                color = [.25, 1, 0, 1]
            elif 55 <= win_rate <= 60:
                color = [0, 1, 0, 1]
            elif 60 <= win_rate <= 75:
                color = [0, 1, .5, 1]
            else:
                color = [0, 1, 1, 1]

            win_rate_label = Label(text=calculated_win_rate_text, size_hint=(None, None), height=self.height / 8, color=color)
            view_button = Button(text="View", size_hint=(None, None), height=self.height / 8, width=self.width / 9)
            view_button.id = str(champion_name)
            view_button.bind(on_press=partial(self.single_champion))
            kda_label = Label(text=calculated_kda_text, size_hint=(None, None), height=self.height / 8)

            self.all_champions_grid_layout.add_widget(view_button)
            self.all_champions_grid_layout.add_widget(champion_name_label)
            self.all_champions_grid_layout.add_widget(champion_image)
            self.all_champions_grid_layout.add_widget(win_rate_label)
            self.all_champions_grid_layout.add_widget(kda_label)

    def save_win_rates(self):
        """
        save_win_rates: Saves all champion data to a single csv file in the summoner's name directory
        :return:
        """

        summoners_path = 'winrate_csv/' + summoner_1.name

        column_1 = []       # Champion Name
        column_2 = []       # Win Rate
        column_3 = []       # Wins
        column_4 = []       # Losses
        column_5 = []       # Kills + Assists
        column_6 = []       # Deaths
        column_7 = round(datetime.datetime.now().timestamp() * 1000.0)

        for entry in self.win_rates:
            for entry2 in self.all_kda:
                if entry == entry2:

                    wins = self.win_rates[entry][0]
                    losses = self.win_rates[entry][1]
                    win_rate = round(((int(wins) / (int(losses) + int(wins))) * 100), 2)
                    kills_assists = self.all_kda[entry2][0]
                    deaths = self.all_kda[entry2][1]

                    column_1.append(entry)
                    column_2.append(win_rate)
                    column_3.append(wins)
                    column_4.append(losses)
                    column_5.append(kills_assists)
                    column_6.append(deaths)
            data = {'champion_name': column_1, 'win_rate': column_2, 'wins': column_3, 'losses': column_4, 'kills_assists': column_5, 'deaths': column_6}
        data['date'] = column_7



        # If data is found for the summoner
        if os.path.isfile(summoners_path + '/all_champions_win_rates.csv'):
            # Removes the old file before creating a new one
            os.remove(summoners_path + '/all_champions_win_rates.csv')

        df = pandas.DataFrame(data=data)
        df.to_csv(summoners_path + '/all_champions_win_rates.csv', header=['champion_name', 'win_rates', 'wins', 'losses', 'kills_assists', 'deaths', 'date'], index=False)

    def sort_by_champion(self):
        """
        sort_by_champion: Sorts all champions alphabetically by the champion name
        :return:
        """
        self.all_champions_grid_layout.clear_widgets()
        df = pandas.read_csv('winrate_csv/' + summoner_1.name + '/all_champions_win_rates.csv')
        if self.champ_sort is False:
            sorted_df = df.sort_values(by=["champion_name"], ascending=True)
            self.champ_sort = True
        else:
            sorted_df = df.sort_values(by=["champion_name"], ascending=False)
            self.champ_sort = False

        os.remove('winrate_csv/' + summoner_1.name + '/all_champions_win_rates.csv')
        sorted_df.to_csv('winrate_csv/' + summoner_1.name + '/all_champions_win_rates.csv', header=['champion_name', 'win_rates', 'wins', 'losses', 'kills_assists', 'deaths', 'date'], index=False)
        self.populate_all_champion_win_rates()

    def sort_by_win_rate(self):
        """
        sort_by_win_rate: Sorts all champions by their win rates
        :return:
        """
        self.all_champions_grid_layout.clear_widgets()
        df = pandas.read_csv('winrate_csv/' + summoner_1.name + '/all_champions_win_rates.csv')
        if self.win_rate_sort is False:
            sorted_df = df.sort_values(by=["win_rates", "wins"], ascending=[False, False])
            self.win_rate_sort = True
        else:
            sorted_df = df.sort_values(by=["win_rates", "wins"], ascending=[True, True])
            self.win_rate_sort = False
        os.remove('winrate_csv/' + summoner_1.name + '/all_champions_win_rates.csv')
        sorted_df.to_csv('winrate_csv/' + summoner_1.name + '/all_champions_win_rates.csv', header=['champion_name', 'win_rates', 'wins', 'losses', 'kills_assists', 'deaths', 'date'], index=False)
        self.populate_all_champion_win_rates()

    def single_champion(self, button):
        """
        single_champion: Changes the screen to the single champion screen
        :param button:
        :return:
        """
        summoner_1.current_champion = button.id
        self.parent.current = "singleChampion"

    def update_all_champions(self):
        """
        update_all_champions: Updates the all_champions csv file based on the last date saved
        :return:
        """
        df = pandas.read_csv('winrate_csv/' + summoner_1.name + '/all_champions_win_rates.csv')
        date = None
        for index, line in df.iterrows():
            date = line['date']
        if date is not None:
            self.last_update = date
        else:
            print("Error: Date is none")
            exit(1)

        self.calculate_win_rates()
        if self.no_new_data is False:
            self.save_win_rates()
            self.populate_all_champion_win_rates()
        else:
            popup = InvalidSearchPopup()
            popup.open_popup_5()
            print("No new data")


# ==========================================================================================
#       Single Champion Gui: All stats about a single champion the summoner plays
# ==========================================================================================
class SingleChampionGui(Screen):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.win_rates = {}
        self.kda = {}
        self.champ_sort = False
        self.win_rate_sort = False

        self.no_new_data = False

        # When season 11 started - Epoch millisecond
        self.last_update = 1610118000000

    def on_enter(self, *args):
        """
        on_enter: Determines what happens when entering the singleChampionGui page
        :param args:
        :return:
        """
        # Clears win rates dictionary and previous loads
        self.single_champion_grid_layout.clear_widgets()

        summoners_path = 'winrate_csv/' + summoner_1.name

        # If no directory is found for the summoner, creates one
        if not os.path.isdir(summoners_path):
            os.mkdir(summoners_path)

        # If data is not found for the summoner
        if not os.path.isfile(summoners_path + '/' + summoner_1.current_champion + '_win_rates.csv'):

            self.calculate_win_rates()
            self.save_win_rates()

        self.populate_single_champion_win_rates()

    def calculate_win_rates(self):
        """
        calculate_win_rates - To calculate and update your champion win rates
        :return:
        """

        # Clears previous data
        self.win_rates = {}
        self.kda = {}

        # Creates champion name to id conversion
        with open('data_dragon_' + data_dragon_version + '/' + data_dragon_version + '/data/en_US/champion.json', 'r', encoding="utf-8") as champion_data:
            champion_dict = json.load(champion_data)
        champion_id_to_name = {}
        for key in champion_dict['data']:
            row = champion_dict['data'][key]
            champion_id_to_name[row['key']] = row['id']

        # Convert the champion name to champion id
        champion_id = champion_dict['data'][summoner_1.current_champion]['key']

        # If there is saved data
        if os.path.isfile('winrate_csv/' + summoner_1.name + '/' + summoner_1.current_champion + '_win_rates.csv'):
            df = pandas.read_csv('winrate_csv/' + summoner_1.name + '/' + summoner_1.current_champion + '_win_rates.csv')
            for index, line in df.iterrows():

                if not pandas.isna(line['champion_name']):
                    champion_name = 'None'
                else:
                    champion_name = line['champion_name']
                wins = line['wins']
                losses = line['losses']
                self.win_rates[champion_name] = [wins, losses]

        url = "https://" + summoner_1.region + ".api.riotgames.com/lol/match/v4/matchlists/by-account/" + summoner_1.account_id + "?champion=" + str(champion_id) + "&queue=420&beginTime=" + str(self.last_update) + "&api_key=" + str(DevelopmentAPIKey)

        account_details = requests.get(url)

        # Checking for 404 error: no new data
        status = account_details.status_code
        account_details = account_details.json()

        if status != 404:
            total_games = account_details['totalGames']
            begin_index = 0

            # Loops through the sets of 100 games
            while begin_index < total_games:
                indexed_url = 'https://' + summoner_1.region + '.api.riotgames.com/lol/match/v4/matchlists/by-account/' + summoner_1.account_id + '?champion=' + str(champion_id) + '&queue=420&beginTime=' + str(self.last_update) + '&beginIndex=' + str(begin_index) + '&api_key=' + str(DevelopmentAPIKey)
                match_history = requests.get(indexed_url)
                match_history = match_history.json()
                matches = match_history['matches']

                # Loops through all matches in match_data
                for match in matches:

                    # Todo Using sleep to delay the calls to riot api
                    sleep(2)
                    print('sleeping 2 seconds')

                    current_champ = match['champion']
                    current_champion_name = champion_id_to_name.get(str(current_champ))

                    game_id = str(match['gameId'])

                    match_lookup = 'https://' + summoner_1.region + '.api.riotgames.com/lol/match/v4/matches/' + game_id + '?api_key=' + str(
                        DevelopmentAPIKey)
                    match_lookup = requests.get(match_lookup)
                    match_lookup = match_lookup.json()

                    # Win is used to find the opposing team (the inverse of whatever win is)
                    win = None

                    # Loops through each player in the match
                    for summoner in match_lookup['participants']:
                        if summoner['championId'] == current_champ:
                            win = summoner['stats']['win']

                    # Loops through each player in the match a second time now know which team has the enemies
                    for summoner in match_lookup['participants']:
                        if summoner['stats']['win'] is not win:

                            # Calculates kda vs enemy champions
                            kills = summoner['stats']['kills']
                            deaths = summoner['stats']['deaths']
                            assists = summoner['stats']['assists']
                            kills_assists = kills + assists

                            # Calculates win percentages vs enemy champions
                            enemy_champ = champion_id_to_name.get(str(summoner['championId']))
                            if enemy_champ in self.win_rates:
                                if win is True:
                                    self.win_rates[enemy_champ][0] = self.win_rates[enemy_champ][0] + 1
                                else:
                                    self.win_rates[enemy_champ][1] = self.win_rates[enemy_champ][1] + 1
                            else:
                                if win is True:
                                    self.win_rates[enemy_champ] = [1, 0]
                                else:
                                    self.win_rates[enemy_champ] = [0, 1]

                            if enemy_champ in self.kda:
                                self.kda[enemy_champ][0] = self.kda[enemy_champ][0] + kills_assists
                                self.kda[enemy_champ][1] = self.kda[enemy_champ][1] + deaths
                            else:
                                self.kda[enemy_champ] = [kills_assists, deaths]

                # Maximum number of games that can be loaded at once is 100
                begin_index += 100

        else:
            self.no_new_data = True

    def save_win_rates(self):
        """
        save_win_rates: Saves single champion data to a single csv file in the summoner's name directory
        :return:
        """

        summoners_path = 'winrate_csv/' + summoner_1.name

        column_1 = []       # Champion Name
        column_2 = []       # Win Rate
        column_3 = []       # Wins
        column_4 = []       # Losses
        column_5 = []       # Kills + Assists
        column_6 = []       # Deaths
        column_7 = round(datetime.datetime.now().timestamp() * 1000.0)

        for entry in self.win_rates:
            for entry2 in self.kda:
                if entry2 == entry:
                    wins = self.win_rates[entry][0]
                    losses = self.win_rates[entry][1]
                    win_rate = round(((int(wins) / (int(losses) + int(wins))) * 100), 2)

                    kills_assists = self.kda[entry2][0]
                    deaths = self.kda[entry2][1]

                    column_1.append(entry)
                    column_2.append(win_rate)
                    column_3.append(wins)
                    column_4.append(losses)
                    column_5.append(kills_assists)
                    column_6.append(deaths)

            data = {'champion_name': column_1, 'win_rate': column_2, 'wins': column_3, 'losses': column_4, 'kills_assists': column_5, 'deaths': column_6}
        data['date'] = column_7

        # If data is found for the summoner
        if os.path.isfile(summoners_path + '/' + summoner_1.current_champion + '_win_rates.csv'):
            # Removes the old file before creating a new one
            os.remove(summoners_path + '/' + summoner_1.current_champion + '_win_rates.csv')

        df = pandas.DataFrame(data=data)
        df.to_csv(summoners_path + '/' + summoner_1.current_champion + '_win_rates.csv', header=['champion_name', 'win_rates', 'wins', 'losses', 'kills_assists', 'deaths', 'date'], index=False)

    def populate_single_champion_win_rates(self):
        """
        populate_single_champion_win_rates: Adds champion data to the grid layout
        :return:
        """

        df = pandas.read_csv('winrate_csv/' + summoner_1.name + '/' + summoner_1.current_champion + '_win_rates.csv')
        for index, line in df.iterrows():

            # Champion Name + Icon
            champion_name = line['champion_name']
            if not pandas.isna(line['champion_name']):
                champion_image = Image(source='data_dragon_' + data_dragon_version + '/' + data_dragon_version + '/img/champion/' + champion_name + '.png',
                                       size_hint=(None, None), height=self.height / 8)
            else:
                champion_image = Image(source='data_dragon_' + data_dragon_version + '/' + data_dragon_version + '/img/champion/None.png', size_hint=(None, None), height=self.height / 8)
            champion_name_label = Label(text=str(champion_name), size_hint=(None, None), height=self.height/8)

            # Converts the string representation of the win rate list list, to a list
            win_rate = line['win_rates']
            wins = line['wins']
            losses = line['losses']

            kills_assists = line['kills_assists']
            deaths = line['deaths']

            if deaths == 0:
                kda = 'Infinite'
            else:
                kda = round((kills_assists/deaths), 2)

            calculated_win_rate_text = str(win_rate) + ' % : (' + str(wins) + ' / ' + str(losses) + ')'
            kda_text = 'KDA: ' + str(kda)

            if win_rate <= 25:
                color = [1, 0, 0, 1]
            elif 25 <= win_rate <= 45:
                color = [1, .5, 0, 1]
            elif 45 <= win_rate <= 50:
                color = [1, 1, 0, 1]
            elif 50 <= win_rate <= 55:
                color = [.25, 1, 0, 1]
            elif 55 <= win_rate <= 60:
                color = [0, 1, 0, 1]
            elif 60 <= win_rate <= 75:
                color = [0, 1, .5, 1]
            else:
                color = [0, 1, 1, 1]

            win_rate_label = Label(text=calculated_win_rate_text, size_hint=(None, None), height=self.height / 8, color=color)
            kda_label = Label(text=kda_text, size_hint=(None, None), height=self.height / 8)

            self.single_champion_grid_layout.add_widget(champion_name_label)
            self.single_champion_grid_layout.add_widget(champion_image)
            self.single_champion_grid_layout.add_widget(win_rate_label)
            self.single_champion_grid_layout.add_widget(kda_label)

    def sort_by_champion(self):
        """
        sort_by_champion: Sorts all champions alphabetically by the champion name
        :return:
        """
        self.single_champion_grid_layout.clear_widgets()
        df = pandas.read_csv('winrate_csv/' + summoner_1.name + '/' + summoner_1.current_champion + '_win_rates.csv')
        if self.champ_sort is False:
            sorted_df = df.sort_values(by=["champion_name"], ascending=True)
            self.champ_sort = True
        else:
            sorted_df = df.sort_values(by=["champion_name"], ascending=False)
            self.champ_sort = False

        os.remove('winrate_csv/' + summoner_1.name + '/' + summoner_1.current_champion + '_win_rates.csv')
        sorted_df.to_csv('winrate_csv/' + summoner_1.name + '/' + summoner_1.current_champion + '_win_rates.csv', header=['champion_name', 'win_rates', 'wins', 'losses', 'kills_assists', 'deaths', 'date'], index=False)
        self.populate_single_champion_win_rates()

    def sort_by_win_rate(self):
        """
        sort_by_win_rate: Sorts all champions by their win rates
        :return:
        """
        self.single_champion_grid_layout.clear_widgets()
        df = pandas.read_csv('winrate_csv/' + summoner_1.name + '/' + summoner_1.current_champion + '_win_rates.csv')
        if self.win_rate_sort is False:
            sorted_df = df.sort_values(by=["win_rates", "wins"], ascending=[False, False])
            self.win_rate_sort = True
        else:
            sorted_df = df.sort_values(by=["win_rates", "losses"], ascending=[True, True])
            self.win_rate_sort = False
        os.remove('winrate_csv/' + summoner_1.name + '/' + summoner_1.current_champion + '_win_rates.csv')
        sorted_df.to_csv('winrate_csv/' + summoner_1.name + '/' + summoner_1.current_champion + '_win_rates.csv', header=['champion_name', 'win_rates', 'wins', 'losses', 'kills_assists', 'deaths', 'date'], index=False)
        self.populate_single_champion_win_rates()








# TODO: updating erased all data








    def update_single_champion(self):
        """
        update_all_champions: Updates the all_champions csv file based on the last date saved
        :return:
        """
        df = pandas.read_csv('winrate_csv/' + summoner_1.name + '/' + summoner_1.current_champion + '_win_rates.csv')
        date = None
        for index, line in df.iterrows():
            date = line['date']
        if date is not None:
            self.last_update = date
        else:
            print("Error: Date is none")
            exit(1)

        self.calculate_win_rates()
        if self.no_new_data is False:
            self.save_win_rates()
            self.populate_single_champion_win_rates()
        else:
            popup = InvalidSearchPopup()
            popup.open_popup_5()
            print("No new data")

# ==========================================================================================
#       Gui Manager:
# ==========================================================================================
class GuiManager(ScreenManager):
    pass


class Summoner:
    def __init__(self):
        self.cass_region = None

        self.region = None
        self.summoner_data = None
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

        self.current_match_id = None
        self.current_champion = None

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
            if len(self.ranked_data) == 0:
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

                    elif self.ranked_data[i]['queueType'] == 'RANKED_FLEX_SR':
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

        print("current_match_id", self.current_match_id)


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
