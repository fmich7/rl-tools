import os, shutil

#Skrypt wymienia mapy w folderze rocketa

pathToMapsFolder = 'maps' #folder z mapami, trzeba tu wrzucić wsztstkie customowe mapy
pathToOriginalMap = 'maps/original map' #folder gdzie trzeba umieścić oryginalną mapę [limit 1-go pliku]
pathToRocketLeagueMaps = r'C:\rocketleague\tagame\...' #folder z mapami rocketa


def main():
    #if tworzy folder jeśli nie istnieją
    if not os.path.exists(pathToMapsFolder):
        os.makedirs(pathToOriginalMap)
    elif not os.path.exists(pathToOriginalMap):
        os.mkdir(pathToOriginalMap)

    originalMapFolderName = pathToOriginalMap.split('/')[-1]
    #sprawdza czy w folderze z oryginalną mapą coś jest
    try:
        originalMapName = os.listdir(pathToOriginalMap)[0]
    except:
        print(f"Original map not found! Check if maps/{originalMapFolderName} exists or if a map is there")
        return
    #printuje nazwy map
    maps = os.listdir(pathToMapsFolder)
    maps.remove(originalMapFolderName)
    mapsName = "[Which map to change] \n0: Reset to default map\n"

    for i in range(len(maps)):
        mapsName += f'{i + 1}: {maps[i]}\n'
    print(mapsName)
    mapToSwap = int(input("Number of choice: "))

    #sprawdza czy folder z mapami rocketa istnieje
    if not os.path.exists(pathToRocketLeagueMaps):
        print(f'\nPath to rocket league map folder is invalid [{pathToRocketLeagueMaps}]')
        return
    #swapowanie map
    if mapToSwap == 0:
        shutil.copy(f"{pathToOriginalMap}/{originalMapName}", f"{pathToRocketLeagueMaps}/{originalMapName}")
        print("Success")
    elif mapToSwap > 0 and mapToSwap <= len(maps):
        shutil.copy(f"{pathToMapsFolder}/{maps[mapToSwap - 1]}", f"{pathToRocketLeagueMaps}/{originalMapName}")
        print("Success")

if __name__ == "__main__":
    main()
