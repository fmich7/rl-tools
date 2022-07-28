# This Python file uses the following encoding: utf-8
import sys, os, shutil, json


from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QScrollArea, QWidget, QVBoxLayout, QListWidget, QLabel, QGraphicsView, QGraphicsPixmapItem, QGraphicsScene
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from threading import Timer

pathToMapsFolder = 'maps' #folder z mapami, trzeba tu wrzucić wsztstkie customowe mapy
pathToOriginalMap = 'maps/original map' #folder gdzie trzeba umieścić oryginalną mapę [limit 1-go pliku]
pathToRocketLeagueMaps = str()  #folder z mapami rocketa/load from config
currentMap = str() #obecna mapa/load from config
originalMapName = 'ThrowbackStadium_P.upk'
mapNotFound = "Nie znalazlo mapy"
selectAnyMapFromList = "Select any map from list"

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('form.ui', self) # Load the .ui file

        self.statusLifetime = 2
        self.status = self.findChild(QLabel, "status")
        self.txt_name = self.findChild(QLabel, "txt_name")
        self.txt_currentMap = self.findChild(QLabel, "txt_currentMap")
        self.btn_change = self.findChild(QPushButton, "btn_change")
        self.img_preview = self.findChild(QGraphicsView, "img_preview")
        self.mapList = self.findChild(QListWidget, "map_list")

        self.color_success = '59, 255, 0'
        self.color_error = '255, 77, 64'

        self.status.setText('')
        self.txt_currentMap.setText("Current map: {}".format(currentMap))
        self.btn_change.clicked.connect(self.replaceMap)
        self.mapList.itemSelectionChanged.connect(self.updateMapInfo)
        self.updateMapList()
        self.show() # Show the GUI

    def replaceMap(self) -> None:
        if not os.path.exists(pathToRocketLeagueMaps):
            self.statusManager(f'\nPath to rocket league map folder is invalid [{pathToRocketLeagueMaps}]', self.color_error)
            return
        elif self.txt_name.text() in [mapNotFound, selectAnyMapFromList]:
            self.statusManager(self.txt_name.text(), self.color_error)
            return
        pathToHighlightedMap = f"{pathToMapsFolder}/{self.mapList.currentItem().text()}/{self.txt_name.text()}"
        shutil.copy(f"{pathToHighlightedMap}", f"{pathToRocketLeagueMaps}/{originalMapName}")

        self.updateConfig(self.txt_name.text())
        self.txt_currentMap.setText("Current map: {}".format(self.txt_name.text()))
        print(pathToHighlightedMap, self.txt_name.text())
        self.statusManager('Mapa została przeniesona')

    def statusManager(self, message: str, color='59, 255, 0') -> None:
        self.status.setText(message)
        self.status.setStyleSheet(f"QLabel {{ color: rgb(   {color}); }}")
        t = Timer(self.statusLifetime, self.resetStatus)
        t.start()

    def resetStatus(self) -> None:
        self.status.setText('')

    #on item change in list
    def updateMapInfo(self) -> None:
        #TODO! self.updateMapList()
        newMap = self.mapList.currentItem().text()
        pathToNewMap = f"{pathToMapsFolder}/{newMap}"
        map_name = str()
        map_preview = str()
        for item in os.listdir(pathToNewMap):
            if item.endswith(('udk', 'upk')):
                map_name = item
            elif item.endswith(('png', 'jpg', 'jpeg')):
                map_preview = item

        if map_name == "":
            map_name = mapNotFound
        #change map name
        self.txt_name.setText(map_name)
        #load image
        scene = QGraphicsScene(self)
        pixmap = QPixmap(f"{pathToNewMap}/{map_preview}")
        pixmap = pixmap.scaled(238, 203) #238/203
        item = QGraphicsPixmapItem(pixmap)
        scene.addItem(item)
        self.img_preview.setScene(scene)
        ################################################
        print(self.mapList.currentItem().text(), os.listdir(pathToNewMap))
    
    #init map dif
    def updateMapList(self) -> None:
        maps = os.listdir(pathToMapsFolder)
        for map in maps:
            if os.path.isdir(f'{pathToMapsFolder}/{map}'):
                self.mapList.addItem(map)

    def updateConfig(self, mapName: str) -> None:
        with open('config.json', 'w') as file:
            data = {}
            data['pathToRocketLeagueMaps'] = pathToRocketLeagueMaps
            data['currentMap'] = mapName
            json.dump(data, file)

def setup() -> None:
    if not os.path.exists(pathToMapsFolder):
        os.makedirs(pathToOriginalMap)
    elif not os.path.exists(pathToOriginalMap):
        os.mkdir(pathToOriginalMap)

    if not os.path.exists('config.json'):
        defaultConfig = {"pathToRocketLeagueMaps": "E:\\gry\\rocketleague\\TAGame\\CookedPCConsole", "currentMap": "default"}
        with open('config.json', 'w') as file:
            json.dump(defaultConfig, file)

    with open('config.json', 'r') as file:
        data = json.load(file)
        global pathToRocketLeagueMaps, currentMap
        pathToRocketLeagueMaps = data['pathToRocketLeagueMaps']
        currentMap = data['currentMap']

if __name__ == "__main__":
    setup()
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())
