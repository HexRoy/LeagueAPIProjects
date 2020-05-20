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
        region = input("Enter your region: BR, EUN, EUW, JP, KR, LA1, LA2, NA, OC, TR, RU \n")
        if region.upper() in region_list:
            loop = False
        else:
            print("Invalid region")
    region = region_conversion[region.upper()]
    return region


# Gets a valid summoner name in the region entered, from the user
def get_summoner_data():

    loop = True

    while loop:
        summoner_name = input("Enter summoner name in the region: " + Region + "\n")
        url = "https://" + Region + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner_name +\
              "?api_key=" + DevelopmentAPIKey
        url_data = requests.get(url)
        code = url_data.status_code
        if code == 200:
            loop = False
        else:
            print("Invalid summoner name")
    return url_data.json()


def get_ranked_data():
    url = "https://" + Region + ".api.riotgames.com/lol/league/v4/entries/by-summoner/" + summonerId + \
          "?api_key=" + DevelopmentAPIKey
    url_data = requests.get(url)
    return url_data.json()


#DevelopmentAPIKey = input("Enter your DEVELOPMENT API KEY")
DevelopmentAPIKey = "RGAPI-5b57ea9d-8ee0-41d7-bdf4-42522552503e"

Region = get_region()
#Region = "NA1"

# Basic summoner data
summonerData = get_summoner_data()
summonerId = summonerData['id']
summonerName = summonerData['name']

# Ranked summoner data: 0 is flex data, 1 is solo/duo data
rankedData = get_ranked_data()

soloTier = rankedData[1]['tier']
soloRank = rankedData[1]['rank']
soloLP = rankedData[1]['leaguePoints']


flexTier = rankedData[0]['tier']
flexRank = rankedData[0]['rank']
flexLP = rankedData[0]['leaguePoints']


print("The Selected Region is: ", Region)
print("Hello, " + summonerName + ":\nSummonerID: (" + summonerId + ")")
print("Your solo/duo rank is:", soloTier, soloRank, soloLP, "LP")
print("Your flex rank is:", flexTier, flexRank, flexLP, "LP")
#TODO
# Extract data from the users profile with given region and summoner name
# Summoner rank, lp, level, champion score
# Calculate matchup win percentages
# https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/HexRoy?api_key=RGAPI-5b57ea9d-8ee0-41d7-bdf4-42522552503e