from PyQt5 import QtCore, QtGui, QtWidgets, uic
import universalisAPI as uapi
import fetchItemIDs as fetch
import sys
import pandas as pd
import json

DC_JSON = uapi.data_centers()
WORLDS = uapi.worlds()
MARKETABLE_ITEMS = uapi.marketable_items()

class GUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()
        uic.loadUi(r'./gui.ui', self)

        self._set_custom_action()
        self.data_center_menu_update()
        self._hide_shortcuts()

        self.show()
        # sys.exit(app.exec_())

    def _set_custom_action(self):
        """
        This prevents problems that can be caused by copying the code created by pyqt convertion
        """
        self.addButton.clicked.connect(self.add_item_by_id)
        self.idList.itemClicked.connect(self.idList_selection)
        self.nameList.itemClicked.connect(self.nameList_selection)
        self.regionComboBox.currentIndexChanged.connect(self.data_center_menu_update)
        self.dcComboBox.currentIndexChanged.connect(self.world_menu_update)
        self.queryButton.clicked.connect(self.test)
        # self.clearButton.clicked.connect(self.default_dc_world_list)

        # Hidden menubar items, because by default there can only be one shortcut assigned
        self.actionAdd.triggered.connect(self.addButton.click)
    
    def _hide_shortcuts(self):
        """
        When setting the title of a menubar title it 'disables' it, but if it is set invisable the items in it cannot be interacted with (even if they have shortcuts set up)
        """
        self.menuShortcuts.setTitle('')

    def add_item_by_id(self):
        text_field = self.itemIdAdd.text()
        if text_field == '':
            # If there is nothing in the entry field it cannot be cast to int
            return

        idnum = int(text_field)
        try:
            item_name = fetch.get_item_name(idnum)
        except:
            # It is posible to enter a number out of the range of items
            return
        
        if item_name == '':
            return

        self.idList.addItem(str(idnum))
        self.nameList.addItem(item_name.title()) # Title capitializes the first leter of each word
    
    def idList_selection(self):
        self.nameList.clearSelection()
    
    def nameList_selection(self):
        self.idList.clearSelection()

    def data_center_menu_update(self):
        region = self.regionComboBox.currentText()
        data_centers = dc_list(region)
        self.dcComboBox.clear()
        self.dcComboBox.addItem('All')
        for i in range(0, len(data_centers)):
            dc = data_centers[i][0]
            self.dcComboBox.addItem(dc)
        self.worldComboBox.addItem('-')

    def world_menu_update(self):
        region = self.regionComboBox.currentText()
        dc = self.dcComboBox.currentText()
        self.worldComboBox.clear()
        if dc == 'All':
            self.worldComboBox.addItem('-')
            return

        self.worldComboBox.addItem('All')
        world_names = world_list(dc, dc_list(region))

        for world in world_names:
            self.worldComboBox.addItem(world)
    

    def test(self):
        return

def dc_json_to_pandas() -> pd.DataFrame:
    """
    This converts the data center json from universalis to a more maintanable DataFrame
    """
    df = pd.read_json(json.dumps(DC_JSON))
    df = df.set_index('region')
    return df

def worlds_json_to_pandas() -> pd.DataFrame:
    """
    This converts the world json from universalis to a more maintanable DataFrame
    """
    df = pd.read_json(json.dumps(WORLDS))
    df = df.set_index('id')
    return df

def dc_list(region_center:str) -> list:
    """
    This function creates a list of data centers that are in a given region
        > 中国 and China will return the same value
    """
    dc_return = []
    _dc_list_ = dc_json_to_pandas().reset_index().to_numpy()

    for dc in _dc_list_:
        if dc[0] == region_center or (dc[0] == '中国' and region_center == 'China'):
            dc_return.append(list(dc[1:]))

    return dc_return

def world_list(data_center:str, dc_info:list) -> list:
    """
    This will split the list of worlds to just those from a single data center
    """
    world_names = worlds_json_to_pandas().T

    for dc in dc_info:
        if dc[0] == data_center:
            return list(world_names[dc[1]].to_numpy()[0])

    return None

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = GUI()
    app.exec_()

    # print('asdfasdfasdf')