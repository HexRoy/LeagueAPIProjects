This repo contains some programs related to the riot game: Leauge of Legands

Useful developer links:
https://developer.riotgames.com/apis
https://developer.riotgames.com/docs/lol
https://developer.riotgames.com/

This app is ran off of Kivy
---------------------------------
If you need to update Kivy:
python -m pip uninstall -y kivy.deps.glew kivy.deps.gstreamer kivy.deps.sdl2 kivy.deps.angle

Otherwise, install:
1.Ensure you have the latest pip, wheel, and virtualenv:
	python -m pip install --upgrade pip wheel setuptools virtualenv
2.Install the dependencies
	python -m pip install docutils pygments pypiwin32 kivy_deps.sdl2==0.1.* kivy_deps.glew==0.1.*
	python -m pip install kivy_deps.gstreamer==0.1.*
3Install kivy:
	python -m pip install kivy==1.11.1