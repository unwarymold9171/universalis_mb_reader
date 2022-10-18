from PyQt5 import QtCore, QtGui, QtWidgets, uic
import universalisAPI as uapi
import fetchItemIDs as fetch
import sys
import re
import os
import pandas as pd
import json

DC_JSON = uapi.data_centers()
WORLDS = uapi.worlds()
MARKETABLE_ITEMS = uapi.marketable_items()

class GUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()
        uic.loadUi(r'./gui.ui', self)

        self.__setup_vars__()

        self.__set_custom_actions__()
        self.data_center_menu_update()
        self.__hide_shortcuts__()

        self.__save_state__()

    def __set_custom_actions__(self) -> None:
        """
        This method helps set up each button to work as expected
        """
        self.addButton.clicked.connect(self.add_item_by_id)
        self.idList.itemClicked.connect(self.idList_selection)
        self.nameList.itemClicked.connect(self.nameList_selection)
        self.regionComboBox.currentIndexChanged.connect(self.data_center_menu_update)
        self.dcComboBox.currentIndexChanged.connect(self.world_menu_update)
        self.queryButton.clicked.connect(self.test)
        # self.clearButton.clicked.connect(self.default_dc_world_list)

        # Hidden menubar items, because by default there can only be one shortcut assigned
        self.actionAdd.triggered.connect(self.add_item_by_id)
    
    def __hide_shortcuts__(self) -> None:
        """
        When setting the title of a menubar title it 'disables' it, but if it is set as hidden the items in it cannot be interacted with
        """
        self.menuShortcuts.setTitle('')

    def __setup_vars__(self) -> None:
        """
        These are variables that will be refrenced when checking an objects last state
        """
        self.region = ''
        self.dc = ''
        self.world = ''
        self.mb_returns = []

    def __save_state__(self, exportState:bool=False) -> None:
        """
        This is saves the current state of the GUI's important elements that may be used later for checking the last state
        """
        self.region = self.regionComboBox.currentText()
        self.dc = self.dcComboBox.currentText()
        self.world = self.worldComboBox.currentText()

        if exportState:
            state = {
                'region': self.region,
                'dc': self.dc,
                'world': self.world
                }
            # TODO Save this as a .json that can be loaded later


    def idList_selection(self) -> None:
        """
        If an element in the idList is selected deselect any selection in nameList
        """
        self.nameList.clearSelection()

    def nameList_selection(self) -> None:
        """
        If an element in the nameList is selected deselect any selection in idList
        """
        self.idList.clearSelection()

    def data_center_menu_update(self) -> None:
        """
        When a region is selected, update the dropdown menu to the data centers from that region
        """
        region = self.regionComboBox.currentText()
        if region == self.region:
            # Check if the new state is the same as the last state
            return
        data_centers = dc_list(region)
        self.dcComboBox.clear()
        self.dcComboBox.addItem('All')
        for i in range(0, len(data_centers)):
            dc = data_centers[i][0]
            self.dcComboBox.addItem(dc)
        self.worldComboBox.addItem('-')
        self.__save_state__()

    def world_menu_update(self) -> None:
        """
        When a data center is selected, update the dropdown menu to the worlds in that data center
        """
        region = self.regionComboBox.currentText()
        dc = self.dcComboBox.currentText()
        if dc == self.dc:
            # Check if the new state is the same as the last state
            return
        self.worldComboBox.clear()
        if dc == 'All':
            self.worldComboBox.addItem('-')
            return

        self.worldComboBox.addItem('All')
        world_names = world_list(dc, dc_list(region))

        for world in world_names:
            self.worldComboBox.addItem(world)
        self.__save_state__()

    def add_item_by_id(self) -> None:
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
        self.nameList.addItem(titlecase(item_name)) # Title capitializes the first leter of each word

        self.itemIdAdd.setText('') # Blank out the entry field if it is able to be added to the list

    def test(self):
        items = self.idList.count()
        item_ids = []
        region = self.regionComboBox.currentText()
        dc = self.dcComboBox.currentText()
        world = self.worldComboBox.currentText()

        for i in range(0, items):
            item_ids.append(self.idList.item(i).text())

        current_mb_data = uapi.retrieve_current_marketboard_data(item_ids, region)
        # print(current_mb_data)

        mb_returns = []
        if items == 1:
            if int(item_ids[0]) in MARKETABLE_ITEMS:
                df_current_data = interperate_current_mb(current_mb_data)

                returns = MarketBoard_Return(self.nameList.item(0).text(),
                    item_ids[0], df_current_data, None, region)
                mb_returns.append(returns)

        else:
            for item_id in item_ids:
                i = item_ids.index(item_id)
                if int(item_id) in MARKETABLE_ITEMS:
                    df_current_data = interperate_current_mb(current_mb_data['items'][item_id])

                    returns = MarketBoard_Return(self.nameList.item(i).text(),
                        item_id, df_current_data, None, region)
                    mb_returns.append(returns)

        self.mb_returns = mb_returns

        for bm_return in mb_returns:
            print(bm_return)
            self.listingsList.addItem(str(bm_return))

        return


class MarketBoard_Return(object):
    """
    This class object acts as a large data container with the current and historical listings and acts as the input for the sub-windows
    """
    def __init__(self, itemName:str, itemID:int, current_marketboard_returns:pd.DataFrame, historical_marketboard_returns:pd.DataFrame, region:str) -> None:
        self.itemName = itemName
        self.itemID = itemID
        self.region = region
        self.listings = Current_Item_Listings(current_marketboard_returns, self.region)
        self.history = None

    def __str__(self) -> str:
        return self.itemName

    def filter_by_dc(self, dcName:str='All'):
        current = self.listings.dc_listings(dcName)
        # TODO history = self.history.dc_listings(dcName)
        return current #, history

    def filter_by_world(self, world:str='All'):
        current = self.listings.world_listings(world)
        # TODO history = self.history.world_listings(world)
        return current #, history

class Current_Item_Listings(object):
    def __init__(self, marketboard_returns:pd.DataFrame, region:str) -> None:
        self.entries = marketboard_returns
        self.region = region

    def dc_listings(self, dcName:str='All') -> pd.DataFrame:
        worldList = []
        df = self.entries
        if not dcName == 'All':
            worldList = world_list(dcName, dc_list(self.region))
            filtered = df.loc[df['World'].isin(worldList)]
            return filtered

        return df

    def world_listings(self, world:str='All'):
        df = self.entries
        if not world == 'All':
            filtered = df.loc[df['World'] == world]
            return filtered
        return df

def titlecase(s:str) -> str:
    """
    This function will work similary to str.title() except for it will only capitalize after a space
    """
    return re.sub(
        r"[A-Za-z]+('[A-Za-z]+)?",
        lambda word: word.group(0).capitalize(),
        s
    )

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

def interperate_current_mb(data:json) -> pd.DataFrame:
    """
    This method takes an individual entry from universalis and translates it into a usable dataframe
        Note: This data is pre-sorted and does not need sorting

    Specifying a dcName requires a region to be set, and will filter entries to only that data center

    Specifying a world name will filter down to only entries from that world otherwise it will check all worlds
    """

    ppu = []
    quantity = []
    worldNames = []
    hq = []
    materia = []
    retainerNames = []
    total = []

    for listing in data['listings']:
        """
        Used entries from the listing: pricePerUnit, quantity, worldName, hq,
            materia, retainerName, total

        Unused entries from the listing: lastReviewTime, stainID, worldID,
            creatorName, creatorID, isCrafted, listingID, onMannequin,
            retainerCity, retainerID, sellerID
        """

        ppu.append(listing['pricePerUnit'])
        quantity.append(listing['quantity'])
        worldNames.append(listing['worldName'])
        hq.append(listing['hq'])
        materia.append(listing['materia'])
        retainerNames.append(listing['retainerName'])
        total.append(listing['total'])

    # Make the dataframe
    mb_data = pd.DataFrame({'Price Per Unit':ppu, 'Quantity':quantity, 'Total':total, 'HQ':hq,
        'Materia':materia, 'Retaner':retainerNames, 'World': worldNames})

    return mb_data
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = GUI()
    window.show()
    app.exec_()

    # print('asdfasdfasdf')