import requests
import json
from bs4 import BeautifulSoup

url_prices = 'https://rl.insider.gg/pl/pc'
id_itemsContainer = 'itemPricesContainer'
dict_paintsToHexColors = dict()
list_paints = list()
list_shortPaints = list()
list_searchedItems = list()

itemsPriceData = dict()

#TODO: fix saving prices, ui, fix same name items error

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
        json.dump(itemsPriceData, file, indent=4)

#recives item container from website
def getPricesContainer():
    site = requests.get(url_prices)
    soup = BeautifulSoup(site.content, 'html.parser')
    items = soup.find(id=id_itemsContainer)

    return items

#find items in container
def getSearchedItems(items: list, priceContainer) -> dict:
    itemsDict = dict()
    className = 'priceRange'
    
    #get price list
    for i in items:
        itemsDict[i] = dict()
        result = list()
        item = priceContainer.find('tr', attrs={'data-itemenglishname':i}).find_all('td', class_=className)

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
    pricesFromDatabase = dict()
    diffColors = ['e01200', '3ea200']
    with open('database.json', 'r') as file:
        pricesFromDatabase = json.load(file)[0]
    #l-tabindex
    for l in range(len(items)):
        for item in pricesFromDatabase:
            for i in pricesFromDatabase[item]:
                difference = int()
                if item not in items[l] or i not in items[l][item] or type(items[l][item][i]['price']) is str:
                    continue
                newPrice = items[l][item][i]['price']
                oldPrice = pricesFromDatabase[item][i]['price']
                if oldPrice is str:
                    continue
                if newPrice != oldPrice:
                    difference = newPrice - oldPrice
                    print(newPrice, oldPrice)
                    color = diffColors[difference > 0]
                    items[l][item][i].update({'color': color, 'difference': difference})
    
    return items

#returns as offer_view
def getInOrderedPrices(priceContainer) -> list:
    dict_pricesInOrdered = list()
    with open('config.json', 'r') as file:
        data = json.load(file)
    items = list()
    for offer in data['items']['my-offers']:
        for item in offer:
            items.append(item)
    prices = getSearchedItems(items, priceContainer)
    my_offers = data["items"]["my-offers"]
    
    for i in range(len(my_offers)):
        temp = dict()
        for item in my_offers[i]:
            temp[item] = dict()
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
    prices = [getSearchedItems(list_searchedItems, getPricesContainer())]
    min_prices = takeMinPriceFromRange(prices)

    global itemsPriceData
    itemsPriceData = min_prices

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
    print(returnInOrderedPricesToServer())

if __name__ == '__main__':
    main()
