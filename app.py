import streamlit as st
import requests
from datetime import datetime

# -----------------------------
# Helpers
# -----------------------------
def sats_to_btc(sats):
    return sats / 100_000_000


# -----------------------------
# API FUNCTIONS
# -----------------------------
def get_latest_block():
    """Fetch the latest mined block from mempool.space."""
    URL = "https://mempool.space/api/blocks"
    response = requests.get(URL)
    block = response.json()[0]
    return block


def get_block_transactions(block_id):
    """Fetch all transactions included in a block."""
    URL = f"https://mempool.space/api/block/{block_id}/txs"
    response = requests.get(URL)
    return response.json()


def compute_biggest_transaction(txs):
    """Add total_vout to each tx and return the biggest one."""
    for tx in txs:
        total_vout = sum(vout["value"] for vout in tx["vout"])
        tx["total_vout"] = total_vout

    biggest = max(txs, key=lambda x: x["total_vout"])
    return biggest


# -----------------------------
# STREAMLIT UI
# -----------------------------
st.title("Bitcoin Latest Block Analyzer")

st.write("A simple tool that fetches the latest Bitcoin block and shows the biggest transaction inside it.")


# User clicks the button
if st.button("Fetch Latest Block"):
    # 1. Fetch latest block
    block = get_latest_block()

    st.subheader("Latest Block Information")
    st.write(f"**Block Height:** {block['height']}")
    st.write(f"**Timestamp:** {datetime.fromtimestamp(block['timestamp'])}")
    st.write(f"**Size:** {block['size']} bytes")
    st.write(f"**Weight:** {block['weight']}")
    st.write(f"**Transaction Count:** {block['tx_count']}")

    # 2. Fetch all transactions in this block
    txs = get_block_transactions(block["id"])

    # 3. Compute the biggest transaction
    biggest = compute_biggest_transaction(txs)

    # 4. Display the biggest transaction
    st.subheader("Biggest Transaction in the Block")
    st.write(f"**TXID:** {biggest['txid']}")
    st.write(f"**Value (BTC):** {sats_to_btc(biggest['total_vout'])}")

    # Optional: show raw JSON nicely
    with st.expander("Show full transaction JSON"):
        st.json(biggest)