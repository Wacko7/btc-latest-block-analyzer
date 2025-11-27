import requests

BASE_URL = "https://mempool.space/api"

def fetch_latest_block():
    return requests.get(f"{BASE_URL}/blocks").json()[0]


def fetch_block_transactions(block_hash):
    return requests.get(f"{BASE_URL}/block/{block_hash}/txs").json()


