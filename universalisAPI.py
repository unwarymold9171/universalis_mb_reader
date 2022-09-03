import json
import requests

# Item ids from in-game ids can be found at: https://github.com/Asvel/ffxiv-lodestone-item-id

# Unerversalis API sites
# All will reply back with a json file

DATA_CENTERS = 'https://universalis.app/api/v2/data-centers'
WORLDS = 'https://universalis.app/api/v2/worlds'
MARKETABLE_ITEMS = 'https://universalis.app/api/v2/marketable'

CURRENT_MB_DATA = 'https://universalis.app/api/v2/'
MB_SALE_HISTORY = 'https://universalis.app/api/v2/history/'

def data_centers() -> json:
    """
    Description
    ------
    Returns all data centers supported by the API.
    """
    api_call = DATA_CENTERS

    url = requests.get(api_call)
    api_return = url.json()

    return api_return

def worlds() -> json:
    """
    Description
    ------
    Returns the IDs and names of all worlds supported by the API.
    """
    api_call = WORLDS

    url = requests.get(api_call)
    api_return = url.json()

    return api_return

def marketable_items() -> json:
    api_call = MARKETABLE_ITEMS

    url = requests.get(api_call)
    api_return = url.json()

    return api_return

def retrieve_current_marketboard_data(item_Ids:list, worldDcRegion:str='North-America', listings:int=None, entries:int=None, noGst:bool=None, hq:bool=None, statsWithin:int=None, entriesWithin:int=None) -> json:
    """
    Description
    ------
    Retrieves the data currently shown on the market board for the requested item and world or data center. Item IDs can be comma-separated in order to retrieve data for multiple items at once.
    
    Params
    ------
    :item_Ids:
    :worldDcRegion:
    :listings:
    :entries:
    :noGst:
    :hq:
    :statsWithin:
    :entriesWithin:
    """
    api_call = CURRENT_MB_DATA + worldDcRegion + '/'

    for item in item_Ids:
        api_call = api_call + str(item) + ','
    
    # Remove the last comma from the api call
    api_call = api_call[0:len(api_call)-1]

    if not(listings==None and entries==None and noGst==None and hq==None and statsWithin==None and entriesWithin==None):
        api_call = api_call + '?'

    #?listings=1&entries=2&noGst=3&hq=4&statsWithin=5&entriesWithin=6

    if not listings == None:
        api_call = api_call + 'listings=' + str(listings)
    if not entries == None:
        api_call = api_call + 'entries=' + str(entries)

    if not noGst == None:
        if noGst:
            api_call = api_call + 'noGst=' + str(1)
        else:
            api_call = api_call + 'noGst=' + str(0)

    if not hq == None:
        if hq:
            api_call = api_call + 'hq=' + str(1)
        else:
            api_call = api_call + 'hq=' + str(0)
    
    if not statsWithin == None:
        api_call = api_call + 'statsWithin=' + str(statsWithin)
    if not entriesWithin == None:
        api_call = api_call + 'entriesWithin=' + str(entriesWithin)

    url = requests.get(api_call)
    api_return = url.json()

    return api_return

def retrieve_marketboard_history(item_Ids:list, worldDcRegion:str='North-America', entriesToReturn:int=None, statsWithin:int=None, entriesWithin:int=None) -> json:
    """
    Description
    ------
    Get the most-recently updated items on the specified world or data center, along with the upload times for each item.

    Params
    ------
    :item_Ids:
    :worldDcRegion:
    :listings:
    :entries:
    :noGst:
    :hq:
    :statsWithin:
    :entriesWithin:
    """
    api_call = MB_SALE_HISTORY + worldDcRegion + '/'

    for item in item_Ids:
        api_call = api_call + str(item) + ','
    
    # Remove the last comma from the api call
    api_call = api_call[0:len(api_call)-1]

    if not(entriesToReturn==None and statsWithin==None and entriesWithin==None):
        api_call = api_call + '?'

    #?listings=1&entries=2&noGst=3&hq=4&statsWithin=5&entriesWithin=6

    if not entriesToReturn == None:
        api_call = api_call + 'listings=' + str(entriesToReturn)
    if not statsWithin == None:
        api_call = api_call + 'statsWithin=' + str(statsWithin)
    if not entriesWithin == None:
        api_call = api_call + 'entriesWithin=' + str(entriesWithin)

    url = requests.get(api_call)
    api_return = url.json()

    return api_return



if __name__ == '__main__':
    current_mb = retrieve_current_marketboard_data([37833], noGst=True, listings=100)
    api_return = retrieve_marketboard_history([37833], entriesToReturn=100)


    print(api_return)