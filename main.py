# Testing out the Riot Game League of Legends API
#       - Geoffroy Penny


# Gets a valid Platform Routing Value region tag from the region entered by the user
def get_region():
    # Converts region name to Platform Routing Value
    region_conversion = {"BR": "BR1",
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

#TODO
# Gets a valid summoner name in the region entered, from the user
def get_summoner_name():
    summonerName = "HexRoy"
    return summonerName

#TODO
# Extract data from the users profile with given region and summoner name
# Summoner rank, lp, level, champion score
# Calculate matchup win percentages
# https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/HexRoy?api_key=RGAPI-5b57ea9d-8ee0-41d7-bdf4-42522552503e

DevelopmentAPIKey = input("Enter your DEVELOPMENT API KEY")
Region = get_region()
SummonerName = input("Enter Summoner Name")
print("The Selected Region is: ", Region)
