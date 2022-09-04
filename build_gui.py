from PyQt5 import QtCore, QtGui, QtWidgets
import gui
import universalisAPI as uapi
import fetchItemIDs as fetch
import sys
import pandas as pd
import json

dcs = uapi.data_centers()
worlds = uapi.worlds()

class GUI(object):
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.ui = gui.Ui_MainWindow()
        self.ui.setupUi(MainWindow)

        self._set_custom_action()
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

    def test(self):
        # selected = self.idList.selectedIndexes()[0].row()
        # print(selected)
        self.ui.dcComboBox.clear()
        self.ui.dcComboBox.addItem('All')
        # self.comboBox_2
        return

def dc_json() -> pd.DataFrame:
    df = pd.read_json(json.dumps(dcs))
    df = df.set_index('region')
    return df

def worlds_json() -> pd.DataFrame:
    df = pd.read_json(json.dumps(worlds))
    df = df.set_index('id')
    return df

def dc_list(data_center:str) -> list:
    dc_return = []
    _dc_list_ = dc_json().to_numpy()

    for dc in _dc_list_:
        if dc[0] == data_center:
            dc_return.append(dc)

    return dc_return

def world_list(data_center:str, dc_info:list) -> list:
    
    return

if __name__ == "__main__":
    # ui = GUI()

    print('asdfasdfasdf')