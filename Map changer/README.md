## <p align="center">**Map changer**</p>
### <p align="center">Allows to play Steam custom maps while playing on Epic Games</p>

<br />

Map changer is a tool written in PyQt that allows you to use Steam custom maps when playing on Epic Games. It swaps `ThrowbackStadium_P.upk` with a custom map of your choice. These maps must have the `.udk` extension in order to work. After swapping, just play on custom.

## Run Locally
To run this project install its dependencies:  
`pip3 install -r requirements.txt`

Copy `ThrowbackStadium_P.upk` from rl installation directory to `maps/original map` in project.

Download maps from Steam using [steamworkshopdownloader.io](https://steamworkshopdownloader.io/) and copy `{mapname}.udk` to a new folder in project directory. Example `maps/map_name/map.udk`. To show the preview image, just paste the file in the same folder as the map.

Finally run `python3 main.pyw`

![preview](https://i.imgur.com/otERVuj.png)