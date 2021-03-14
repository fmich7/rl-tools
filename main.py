import requests
import json
import copy
from bs4 import BeautifulSoup

url_prices = 'https://rl.insider.gg/pl/pc'
id_itemsContainer = 'itemPricesContainer'
dict_paintsToHexColors = dict()
list_paints = list()
list_shortPaints = list()
list_searchedItems = list()

itemsPriceData = None
_priceContainer = None

#loads settings from config
def loadSettingsFromConfig() -> None:
    global dict_paintsToHexColors, list_paints, list_shortPaints, list_searchedItems
    with open("config.json", 'r') as file:
        data = json.load(file)
        dict_paintsToHexColors = data['settings']['dict_paintsToHexColors']
        list_paints = data['settings']['list_paints']
        list_shortPaints = data['settings']['list_shortPaints']
        list_searchedItems = data['items']['all-items']

#saves current data to database
def savePricesToDatabase() -> None:
    with open('database.json', 'w') as file:
        file.truncate(0)
        file.seek(0)
        global itemsPriceData
        json.dump(itemsPriceData, file, indent=4)

#recives item container from website
def getPricesContainer():
    global _priceContainer
    if _priceContainer is not None:
        return _priceContainer

    site = requests.get(url_prices)
    soup = BeautifulSoup(site.content, 'html.parser')
    container = soup.find(id=id_itemsContainer)
    _priceContainer = container

    return container

#find items in container
#items {"normal-items" : list, "special-items": list(dict)}
def getSearchedItems(items: dict, priceContainer) -> dict:
    itemsDict = dict()
    className = 'priceRange'
    #list
    for i in items["normal-items"]:
        item = priceContainer.find('tr', attrs={'data-itemenglishname':i})
        if item is None:
            items["normal-items"].remove(i)
            continue
        item = item.find_all('td', class_=className)
        itemsDict[i] = dict()
        result = list()

        for prices in item:
            if 'invisibleColumn' in str(prices):
                continue
            
            #'k' contains price range
            priceDict = json.loads(prices.get('data-info'))
            if priceDict is not None and 'pc' in priceDict['k']:
                priceRange = priceDict['k']['pc']
            else:
                priceRange = "-"
            
            result.append(priceRange)
        
        #fill blank paint prices [ncoloritem]
        while len(result) < len(list_paints):
            result.append('-')
        
        for j in range(len(list_paints)):
            itemsDict[i].update({list_paints[j]: {'price': result[j]}})
    #dict
    for i in items["special-items"]:
        item_name = list(i.keys())[0]
        item = priceContainer.find('tr', attrs={'data-itemenglishname':item_name, 'data-itemrarity':f'|{i[item_name]["rarity"]}|'})
        if item is None:
            items["special-items"].remove(i)
            continue
        #item = item.find('tr', attrs={'data-itemrarity':f'|{i[item_name]["rarity"]}|'})
        item = item.find_all('td', class_=className)
        itemsDict[item_name] = dict()
        result = list()

        for prices in item:
            if 'invisibleColumn' in str(prices):
                continue
            
            #'k' contains price range
            priceDict = json.loads(prices.get('data-info'))
            if priceDict is not None and 'pc' in priceDict['k']:
                priceRange = priceDict['k']['pc']
            else:
                priceRange = "-"
            
            result.append(priceRange)
        
        #fill blank paint prices [ncoloritem]
        while len(result) < len(list_paints):
            result.append('-')
        
        for j in range(len(list_paints)):
            itemsDict[item_name].update({list_paints[j]: {'price': result[j]}})
    return itemsDict

#take minimum price and update the list
def takeMinPriceFromRange(items: list) -> list:
    
    for i in range(len(items)):
        for item in items[i]:
            for color in items[i][item]:
                minPrice = items[i][item][color]['price']
                if type(minPrice) is list:
                    minPrice = minPrice[0]
                items[i][item][color].update({'price': minPrice})
    
    return items

#calculates price below min one -[value]
def calculateQuickSellPrice(items: list, value: int) -> list:
    for i in range(len(items)):
        for item in items[i]:
            for color in items[i][item]:
                minPrice = items[i][item][color]['price']
                if type(minPrice) is not int:
                    continue
                quickSellPrice = minPrice - value
                items[i][item][color].update({'price': quickSellPrice})
    
    return items

#compares current price with old one, and updates item with new informations
def checkPriceDiffWithDatabase(items: list) -> dict:
    newItemsDict = items

    pricesFromDatabase = dict()
    diffColors = ['e01200', '3ea200']
    try:
        with open('database.json', 'r') as file:
            pricesFromDatabase = json.load(file)[0]
    except json.decoder.JSONDecodeError:
        return newItemsDict
    #l-tabindex
    for l in range(len(newItemsDict)):
        for item in pricesFromDatabase:
            for i in pricesFromDatabase[item]:
                difference = int()
                if item not in newItemsDict[l] or i not in newItemsDict[l][item] or type(newItemsDict[l][item][i]['price']) is str:
                    continue
                newPrice = newItemsDict[l][item][i]['price']
                oldPrice = pricesFromDatabase[item][i]['price']
                if oldPrice is str:
                    continue
                if newPrice != oldPrice:
                    difference = newPrice - oldPrice
                    color = diffColors[difference > 0]
                    newItemsDict[l][item][i].update({'color': color, 'difference': difference})
    
    return newItemsDict

#returns as offer_view
def getInOrderedPrices(priceContainer) -> list:
    dict_pricesInOrdered = list()
    with open('config.json', 'r') as file:
        data = json.load(file)

    #which items are searched?
    items_normal = list()
    items_special = list()
    my_offers = data["items"]["my-offers"]
    for offer in my_offers:
        for item in offer:
            if type(offer[item]) is dict:
                items_special.append({item: offer[item]})
            else:
                items_normal.append(item)
    items = {"normal-items": items_normal, "special-items": items_special}
    prices = getSearchedItems(items, priceContainer)
    
    for i in range(len(my_offers)):
        temp = dict()
        for item in my_offers[i]:
            #skips item if it's not existing in data
            if item not in prices:
                continue

            temp[item] = dict()
            if type(my_offers[i][item]) is dict:
                paints = my_offers[i][item]['paints'].split('-')
            else:
                paints = my_offers[i][item].split('-')
            full_paintNames = [list_paints[list_shortPaints.index(x)] for x in paints]
            for paint in list_paints:
                if paint in full_paintNames:
                    itemPrice = prices[item][paint]['price']
                else:
                    continue
                temp[item].update({paint: {'price': itemPrice}})
        dict_pricesInOrdered.append(temp)
            
    return dict_pricesInOrdered

#returns as list_view
def returnListedPricesToServer(priceReduction = 100) -> dict:
    items = {"normal-items": list_searchedItems, "special-items": list()}
    prices = [getSearchedItems(items, getPricesContainer())]
    min_prices = takeMinPriceFromRange(prices)

    global itemsPriceData
    itemsPriceData = copy.deepcopy(min_prices)

    checkedPrices = checkPriceDiffWithDatabase(min_prices)
    firm_prices = calculateQuickSellPrice(checkedPrices, priceReduction)
    
    return firm_prices

#returns as offer_view
def returnInOrderedPricesToServer(priceReduction = 100) -> dict:
    prices = getInOrderedPrices(getPricesContainer())
    min_prices = takeMinPriceFromRange(prices)
    checkedPrices = checkPriceDiffWithDatabase(min_prices)
    firm_prices = calculateQuickSellPrice(checkedPrices, priceReduction)
    
    return firm_prices

loadSettingsFromConfig()

def main():
    returnListedPricesToServer()
    #savePricesToDatabase()

if __name__ == '__main__':
    main()
