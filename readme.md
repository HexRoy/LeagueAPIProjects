# LeagueLookup
## The Best League of Legends Analysis Tool

Useful developer links:
* https://developer.riotgames.com/apis
* https://developer.riotgames.com/docs/lol
* https://developer.riotgames.com/
* https://kivy.org/doc/stable/

This app uses:
* Kivy for the GUI
* Cassiopeia a Python adaptation of the Riot Games League of Legends API:
Jason Maldonis, Rob Rua, Eric Carmichael, Johannes Christ, Anton Pohli, Francesco Zoffoli, … Alex Palmer. (2019, November 1). meraki-analytics/cassiopeia: v4.0.5 (Version v4.0.5). Zenodo. http://doi.org/10.5281/zenodo.3524689
---------------------------------
If you need to update Kivy:
python -m pip uninstall -y kivy.deps.glew kivy.deps.gstreamer kivy.deps.sdl2 kivy.deps.angle

Otherwise, install:
* 1.Ensure you have the latest pip, wheel, and virtualenv:
	python -m pip install --upgrade pip wheel setuptools virtualenv
* 2.Install the dependencies
	python -m pip install docutils pygments pypiwin32 kivy_deps.sdl2==0.1.* kivy_deps.glew==0.1.*
	python -m pip install kivy_deps.gstreamer==0.1.*
* 3.Install kivy:
	python -m pip install kivy==1.11.1

### Table Of Contents
1. [Home GUI](#home-gui)	
* Summoner search bar, with a scrollable region select
* Search favorites and search history 
2. [Profile GUI](#profile-gui) 
* Displays Solo/Flex ranks
* Displays Win/Losses
* Scrollable match history containing Level, KDA, CS, items, game length
* Able to view any match in further detail with 'View Match' button
3. [Match GUI](#match-lookup-gui)
* More detailed stats about a single game
4. [All Champion GUI](#all-champion-stats-gui)
* Win percentages with all champions the summoner has used in ranked games
* Ability to sort alphabetically or by number of win/losses
5. [Single Champion GUI](#single-champion-stats-gui)
* Win percentages of a single champion against other
* Ability to sort alphabetically or by number of win/losses

# Home GUI
 ![alt text](https://github.com/HexRoy/LeagueAPIProjects/blob/master/images/githubrepo/homegui.png)
[Table of contents](#table-of-contents)
# Profile GUI
 ![alt text](https://github.com/HexRoy/LeagueAPIProjects/blob/master/images/githubrepo/profilegui.png)
[Table of contents](#table-of-contents)
# Match Lookup GUI
 ![alt text](https://github.com/HexRoy/LeagueAPIProjects/blob/master/images/githubrepo/matchlookupgui.png)
[Table of contents](#table-of-contents)
# All Champion Stats GUI
 ![alt text](https://github.com/HexRoy/LeagueAPIProjects/blob/master/images/githubrepo/allchampionstatsgui.png)
[Table of contents](#table-of-contents)
# Single Champion Stats GUI
 ![alt text](https://github.com/HexRoy/LeagueAPIProjects/blob/master/images/githubrepo/singlechampstatsgui.png)
[Table of contents](#table-of-contents)