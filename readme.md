# LeagueLookup
## The Best League of Legends Analysis Tool

Useful developer links:
* https://developer.riotgames.com/apis
* https://developer.riotgames.com/docs/lol
* https://developer.riotgames.com/
* https://kivy.org/doc/stable/

This app is ran off of Kivy
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
* Display a Match History


	
# Home GUI
 ![alt text](https://github.com/HexRoy/LeagueAPIProjects/blob/master/images/githubrepo/homegui.png)
[Table of contents](###table-of-contents)
# Profile GUI
 ![alt text](https://github.com/HexRoy/LeagueAPIProjects/blob/master/images/githubrepo/profilegui.png)
[Table of contents](###table-of-contents)

 

 * Users Profile
 ranks
 mmr ?
 match history
 
 
 * Live Game
 match ups
 win percentages/ win percentages on and against those champs
 click on champs to get tips/ against then. your champ tips for them in mini popup
 
 
 * Champion overview 
 win rates on all champs (sortable by win rate/ games played/ kda/ farm)
 able to click any champion and see stats per champ (win rates vs. other champs)
