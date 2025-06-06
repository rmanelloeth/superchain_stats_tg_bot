from web3 import AsyncWeb3
from web3.providers.async_rpc import AsyncHTTPProvider

# Словарь сетей: chain_id → RPC URL
NETWORKS = {
    8453: "https://base.llamarpc.com",         # Base
    10:   "https://0xrpc.io/op",     # Optimism
    130:  "https://unichain.drpc.org",         # Unichain
    57073: "https://ink.drpc.org",             # Ink
    1868:  "https://soneium.drpc.org"          # Soneium
}

async def get_tx_counts_all_chains(address: str) -> dict[int, int | str]:
    results = {}

    for chain_id, rpc in NETWORKS.items():
        try:
            w3 = AsyncWeb3(AsyncHTTPProvider(rpc))

            if not w3.is_address(address):
                results[chain_id] = "❌ invalid address"
                continue

            tx_count = await w3.eth.get_transaction_count(address)
            results[chain_id] = tx_count
        except Exception as e:
            results[chain_id] = f"⚠️ error: {str(e)}"

    return results
