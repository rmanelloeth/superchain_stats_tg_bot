from web3 import AsyncWeb3
from web3.providers.async_rpc import AsyncHTTPProvider

# Словарь сетей: chain_id → RPC URL
NETWORKS = {
    'OPTIMISM': "https://optimism-rpc.publicnode.com",         # OPTIMISM
    'BASE': "https://mainnet.base.org",                 # Base
    'INK': "https://ink.drpc.org",                   # INK
    'SONEIUM':  "https://rpc.soneium.org",           # Soneium
    'LISK':  "https://lisk.drpc.org",                # Lisk
    'UNICHAIN':  "https://unichain.drpc.org"         # Unichnain
}

async def get_tx_counts_all_chains(address: str) -> dict[int, int | str]:
    results = {}

    for chain, rpc in NETWORKS.items():
        try:
            w3 = AsyncWeb3(AsyncHTTPProvider(rpc))

            if not w3.is_address(address):
                results[chain] = "❌ invalid address"
                continue

            tx_count = await w3.eth.get_transaction_count(address)
            results[chain] = tx_count
        except Exception as e:
            results[chain] = f"⚠️ error: {str(e)}"

    return results
