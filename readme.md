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
* Scrollable match history containing Level, KDA, CS, items, game length
* Able to view any match in further detail with 'View Match' button

* Future Functionality: Champion Stats button, Ranked Flex button, Ranked Solo button, Live Game button
3. Match GUI
4. Champion GUI
5. Ranked Flex GUI
6. Ranked Solo GUI
7. Live Game GUI
	
# Home GUI
 ![alt text](https://github.com/HexRoy/LeagueAPIProjects/blob/master/images/githubrepo/homegui.png)
[Table of contents](#table-of-contents)
# Profile GUI
 ![alt text](https://github.com/HexRoy/LeagueAPIProjects/blob/master/images/githubrepo/profilegui.png)
[Table of contents](#table-of-contents)