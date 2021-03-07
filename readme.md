# RL-pricetracker
RL-pricetracker is a small python website made in Flask that fetches data from [rl.insider.gg](https://rl.insider.gg/). The main purpose of this project is to help saving your time. It shows which items' price have changed. Extremely useful when you have many trade offers, and you don't want to waste your time on updating them.

## Setup
To run this project install its dependecies:  
`$ pip3 install -r requirements.txt`  
When it's done run server.py and open **127.0.0.1:5000/** in your browser:  
` $ python3 server.py `

## To-do list
* ~~Add support for selecting items by it's rarity~~
* Reciving items from data optimization
* ~~Fix saving prices to file~~
* Make website look better 
* ~~Container caching~~
* ~~Add tests~~

## Known issues
* ~~Sometimes checkPriceDiffWithDatabase() is crashing, to fix it just wipe out `database.json` and modify returnListedPricesToServer() to skip that function~~

## Screenshots
![List view](https://i.imgur.com/Mdnid8n.png "List view")
![Offers view](https://i.imgur.com/MCOqD34.png "Offers view")
