# RL-pricetracker
RL-pricetracker is a small python website made in Flask that fetches data from [rl.insider.gg](https://rl.insider.gg/). The main purpose of this project is to help saving your time. It shows which items' price have changed. Extremely useful when you have many trade offers, and you don't want to waste your time on updating them.

## Setup
To run this project install its dependecies:  
`$ pip3 install -r requirements.txt`  
When it's done run server.py and open **127.0.0.1:5000/** in your browser:  
` $ python3 server.py `  
Or just run `run.sh`

## To-do list
* Optimize receiving prices from website

## Usage
To change offers edit `config.json`  
```json
"my-offers":[
    {
        "_comment": "max 10 items/paints, paints: no-bl-tw-gr-cr-pi-co-sb-bs-sa-li-fo-or-pu",
        "Dueling Dragons": "no-bl-pi-fo",
        "OEM": {"paints": "bl", "rarity": "veryRare"}
    }
]
```
To add an item to list view edit the same file
```json
"all-items":[
    "Dueling Dragons",
    "New item"
],
```
## Screenshots
![List view](https://i.imgur.com/7QPGAYP.png "List view")
![Offers view](https://i.imgur.com/rlSJ8Ge.png "Offers view")
