import requests
import json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

retry_strategy = Retry(
  total=3,
  backoff_factor=1
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)
wallet_unspent = "/wallet/boxes/unspent"

def get_my_boxes(node_url,address,limit,headers): # get my boxes and LP pool boxes
    #print(address)
    params = {
        "minConfirmations": -1, #-1 includes mempool
        "maxConfirmations": -1,
        "minInclusionHeight": 0,
        "maxInclusionHeight": -1,
        "limit": limit
    }
    my_boxes = []

    #request unspent boxes from node
    response = http.get(node_url+wallet_unspent, headers=headers, params=params)

    if response.status_code == 200:
        # The response content is in response.text
        unspent=response.json()
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

    #get boxIDs and append to my_boxes list
    for box_data in unspent:
        if 'box' in box_data and address in box_data['address'] and 'boxId' in box_data['box']:
            my_boxes.append(box_data['box']['boxId'])

    #get my erg balance
    nanoerg = 0
    for box_data in unspent:
        if 'box' in box_data and address in box_data['address'] and 'value' in box_data['box']:
            nanoerg += box_data['box']['value']
    #print("My boxes",my_boxes)
    return(my_boxes)

def box_to_byte(box_ids,node_url):
    box_bytes = []  # initiate list
    for box_id in box_ids:
        data = http.get(node_url+"/utxo/withPool/byIdBinary/" + box_id)
        data = data.json()
        box_bytes.append(data["bytes"])

    return (box_bytes)

def box_value(node_url,box_id):
    
    response = requests.get(node_url+"/utxo/withPool/byId/"+box_id)
    response_json = response.json()
    data = json.dumps(response_json, indent=4)
    data = json.loads(data)
    value = data['value']
    
    return (value)


