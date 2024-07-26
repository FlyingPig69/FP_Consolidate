# FP_Consolidate
# Consolidate ergo boxes
# Requires the wallet to be set up on an indexed ergo node

import requests
from functions import get_boxes, tx_assembler
import time
import json

node_url = "http://127.0.0.1:9054" #your indexed node
my_address = "" # your address which exists on the indexed node
node_api_key = "" #NODE API KEY

no_boxes = 1000 # no of boxes to consolidate at a time
mining_fee = 0.001 #mininng fee
boxes_threshold = 50 # only consolidate if there are more boxes than this value

interval = 5 # seconds to wait between checking boxes again, if more boxes need to be consolidated will chain the tx

# ---------------NO NEED TO CHANGE ANYTHING BELOW THIS LINE--------------
post_tx =(node_url + "/wallet/transaction/send")
mining_fee = mining_fee*1000000000 #converts mining fee to nanoerg
headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "api_key": node_api_key
}
while True:
    #get my boxes
    box_ids = get_boxes.get_my_boxes(node_url, my_address, no_boxes)
    number_of_boxes = len(box_ids)
    print(time.strftime("%Y-%m-%d %H:%M:%S"),"Unspent boxes:", number_of_boxes)
    if number_of_boxes > boxes_threshold:
        print("Converting", number_of_boxes, "boxes to binary....")
        print("Getting box values....")
        total_value = 0
        for box in box_ids:
            value = get_boxes.box_value(node_url, box)
            total_value += value
        print("Total value is:", value/1000000000, "ERG")

        value_to_send = value - mining_fee
        box_bytes = get_boxes.box_to_byte(box_ids, node_url)

        print("Assembling transaction")
        transaction_to_sign = tx_assembler.consolidate(my_address, box_bytes, mining_fee, value_to_send)

        print("Creating TX")
        tx = json.dumps(transaction_to_sign, indent=4)

        print("Submitting Transaction")
        response = requests.post(url=post_tx, data=tx, headers=headers)
        data = response.json()
        print(data)

    time.sleep(5)