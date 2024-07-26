
def consolidate(my_address,box_bytes,mining_fee,total_value):
    transaction_to_sign = {
        "requests": [
            {
                "address": my_address,
                "value": total_value,
                "assets": [
                ],
                "registers": {
                }
            }
        ],
        "fee": mining_fee,
        "inputsRaw": box_bytes,
        "dataInputsRaw": [
        ]
    }
    return transaction_to_sign