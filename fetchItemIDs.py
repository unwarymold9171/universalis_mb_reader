import pandas as pd
import requests

CSV = 'https://raw.githubusercontent.com/xivapi/ffxiv-datamining/master/csv/Item.csv'
LODESTONE_ITEM_URLID = 'https://raw.githubusercontent.com/Asvel/ffxiv-lodestone-item-id/master/lodestone-item-id.txt'

LODESTONE_BASE_URL = 'https://na.finalfantasyxiv.com/lodestone/playguide/db/item/'

__lodestone_info = pd.read_csv(CSV, sep=',', low_memory=False, header=1, skiprows=[2,3], index_col=[0])

# __lodestone_urls = pd.read_csv(LODESTONE_ITEM_URLID, low_memory=False, header=None) # Pandas skips blank lines
__lodestone_urls = requests.get(LODESTONE_ITEM_URLID).text.splitlines()


def fetch_lodestone_page(itemID:int) -> str:
    url_id = __lodestone_urls[itemID-1]
    url = LODESTONE_BASE_URL + url_id
    return url

def get_item_name(itemID:int):
    if __lodestone_urls[itemID-1] == '':
        return ''

    item_info = __lodestone_info.T[itemID]

    return item_info['Singular']



if __name__ == '__main__':

    print(__lodestone_info)
    print(__lodestone_urls)

    # 37833 (Ilmenite Ingot) = 9288158e865
    print(fetch_lodestone_page(37833))
    print(get_item_name(37833))
