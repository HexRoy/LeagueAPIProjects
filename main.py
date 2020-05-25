# Testing out the Riot Game League of Legends API
#       - Geoffroy Penny

import requests


# Gets a valid Platform Routing Value region tag from the region entered by the user
def get_region():
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
    region_list = ["BR", "EUN", "EUW", "JP", "KR", "LA1", "LA2", "NA", "OC", "TR", "RU"]

    loop = True

    # Loop to make sure a valid region is entered
    while loop:
        region_input = input("Enter your region: BR, EUN, EUW, JP, KR, LA1, LA2, NA, OC, TR, RU \n")
        if region_input.upper() in region_list:
            region_input = region_conversion[region_input.upper()]
            return region_input
        else:
            print("Invalid region")


# Gets a valid summoner name in the region entered, from the user
def get_summoner_data():

    loop = True

    while loop:
        name = input("Enter summoner name in the region: " + region + "\n")
        url = "https://" + region + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + name +\
              "?api_key=" + DevelopmentAPIKey
        url_data = requests.get(url)
        code = url_data.status_code
        if code == 200:
            return url_data.json()
        else:
            print("Invalid summoner name")


# Gets the summoners ranked ranks
def get_ranked_data():
    url = "https://" + region + ".api.riotgames.com/lol/league/v4/entries/by-summoner/" + summoner_id + \
          "?api_key=" + DevelopmentAPIKey
    url_data = requests.get(url)
    return url_data.json()


# Gets the summoners match history
def get_match_history():
    url = "https://" + region + ".api.riotgames.com/lol/match/v4/matchlists/by-account/" + account_id +\
          "?api_key=" + DevelopmentAPIKey
    print(url)
    url_data = requests.get(url)
    return url_data.json()


# DevelopmentAPIKey = input("Enter your DEVELOPMENT API KEY")
DevelopmentAPIKey = "RGAPI-897e2260-3004-4581-98c8-22ff4d26c36f"

region = get_region()
# Region = "NA1"

# Basic summoner data
summoner_data = get_summoner_data()
summoner_id = summoner_data['id']
account_id = summoner_data['accountId']
summoner_name = summoner_data['name']
summoner_level = summoner_data["summonerLevel"]

# Ranked summoner data: 0 is flex data, 1 is solo/duo data
ranked_data = get_ranked_data()
solo_tier = ranked_data[0]['tier']
solo_rank = ranked_data[0]['rank']
solo_lp = ranked_data[0]['leaguePoints']
flex_tier = ranked_data[1]['tier']
flex_rank = ranked_data[1]['rank']
flex_lp = ranked_data[1]['leaguePoints']

# Match history data
match_history = get_match_history()
print(match_history)

# Prints statements
print("The Selected Region is: ", region)
print("Hello, " + summoner_name                          # Prints Summoner name
      + "\nLvl:", summoner_level,                        # Summoner level
      "\nSummonerID: (" + summoner_id + ")"              # Summoner Id
      + "\nAccountID: (" + account_id + ")")             # Account id

print("Your solo/duo rank is:", solo_tier, solo_rank, solo_lp, "LP")
print("Your flex rank is:", flex_tier, flex_rank, flex_lp, "LP")

# TODO
#  Add main + add params for each function after testing.
#  Create gui + nice graphics
#  add win/loss streak
#  add most played champ
#  Extract data from the users profile with given region and summoner name
#  Summoner rank, lp, level, champion score
#  Calculate match up win percentages
#  https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/HexRoy?api_key=RGAPI-5b57ea9d-8ee0-41d7-bdf4-42522552503e
