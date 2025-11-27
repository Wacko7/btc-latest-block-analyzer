import json
from datetime import datetime
import requests

def sats_to_btc(sats):
    return sats / 100_000_000

URL = "https://mempool.space/api/blocks"
response = requests.get(URL)
block = response.json()[0]  # Get the latest block  
size= block["size"]
weight= block["weight"]
tx_count= block["tx_count"]

URL_tx= f"https://mempool.space/api/block/{block['id']}/txs"
response_tx = requests.get(URL_tx)
txs = response_tx.json()

for tx in txs:
    total_vout = sum(vout["value"] for vout in tx["vout"])
    tx['total_vout'] = total_vout

biggest_tx = sorted(txs, key=lambda x: x['total_vout'], reverse=True)[: 1]  # Top 1 biggest transaction
clean_biggest_txs = [
    {
        "txid": tx["txid"],
        "value_btc": sats_to_btc(tx["total_vout"])
    }
    for tx in biggest_tx
]
block_data = {
    "block_height": block["height"],
    "timestamp": datetime.fromtimestamp(block["timestamp"]).isoformat(),
    "size": size,
    "weight": weight,
    "tx_count": tx_count,
    "biggest_transactions":clean_biggest_txs
}

with open("block_summary.json", "w") as f:
    json.dump(block_data, f, indent=4)

print(block_data, indent=4)