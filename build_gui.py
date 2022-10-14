from PyQt5 import QtCore, QtGui, QtWidgets
import gui
import universalisAPI as uapi
import fetchItemIDs as fetch
import sys
import pandas as pd
import json

DC_JSON = uapi.data_centers()
WORLDS = uapi.worlds()
MARKETABLE_ITEMS = uapi.marketable_items()

class GUI(object):
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.ui = gui.Ui_MainWindow()
        self.ui.setupUi(MainWindow)

        self._set_custom_action()
        self.data_center_menu_update()
        self._hide_shortcuts()

        MainWindow.show()
        sys.exit(app.exec_())

    def _set_custom_action(self):
        """
        This prevents problems that can be caused by copying the code created by pyqt convertion
        """
        self.ui.addButton.clicked.connect(self.add_item_by_id)
        self.ui.idList.itemClicked.connect(self.idList_selection)
        self.ui.nameList.itemClicked.connect(self.nameList_selection)
        self.ui.regionComboBox.currentIndexChanged.connect(self.data_center_menu_update)
        self.ui.dcComboBox.currentIndexChanged.connect(self.world_menu_update)
        # self.ui.clearButton.clicked.connect(self.default_dc_world_list)

        # Hidden menubar items, because by default there can only be one shortcut assigned
        self.ui.actionAdd.triggered.connect(self.ui.addButton.click)
    
    def _hide_shortcuts(self):
        """
        When setting the title of a menubar title it 'disables' it, but if it is set invisable the items in it cannot be interacted with (even if they have shortcuts set up)
        """
        self.ui.menuShortcuts.setTitle('')

    def add_item_by_id(self):
        idnum = int(self.ui.itemIdAdd.text())
        try:
            item_name = fetch.get_item_name(idnum)
        except:
            # It is posible to enter a number out of the range of items
            return
        
        if item_name == '':
            return

        self.ui.idList.addItem(str(idnum))
        self.ui.nameList.addItem(item_name)
    
    def idList_selection(self):
        self.ui.nameList.clearSelection()
    
    def nameList_selection(self):
        self.ui.idList.clearSelection()

    def data_center_menu_update(self):
        region = self.ui.regionComboBox.currentText()
        data_centers = dc_list(region)
        self.ui.dcComboBox.clear()
        self.ui.dcComboBox.addItem('All')
        for i in range(0, len(data_centers)):
            dc = data_centers[i][0]
            self.ui.dcComboBox.addItem(dc)
        self.ui.worldComboBox.addItem('-')

    def world_menu_update(self):
        region = self.ui.regionComboBox.currentText()
        dc = self.ui.dcComboBox.currentText()
        self.ui.worldComboBox.clear()
        if dc == 'All':
            self.ui.worldComboBox.addItem('-')
            return

        self.ui.worldComboBox.addItem('All')
        world_names = world_list(dc, dc_list(region))

        for world in world_names:
            self.ui.worldComboBox.addItem(world)
    
    # def default_dc_world_list(self):
    #     region = self.ui.regionComboBox.currentText()
    #     data_centers = dc_list(region)
    #     self.ui.dcComboBox.addItem('All')
    #     for i in range(0, len(data_centers)):
    #         dc = data_centers[i][0]
    #         self.ui.dcComboBox.addItem(dc)
    #     self.ui.worldComboBox.addItem('-')

    def test(self):
        # selected = self.idList.selectedIndexes()[0].row()
        # print(selected)
        # print(self.ui.regionComboBox.currentText())
        # self.ui.dcComboBox.clear()
        # self.ui.dcComboBox.addItem('All')
        # self.comboBox_2
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
    ui = GUI()

    # print('asdfasdfasdf')