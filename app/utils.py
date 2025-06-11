import aiohttp
import random
from web3 import AsyncWeb3
from web3.providers.async_rpc import AsyncHTTPProvider

# Загрузка прокси из файла

# Словарь сетей
NETWORKS = {
    'OPTIMISM': "https://optimism-rpc.publicnode.com",
    'BASE': "https://mainnet.base.org",
    'INK': "https://ink.drpc.org",
    'SONEIUM':  "https://soneium.drpc.org",
    'LISK':  "https://lisk.drpc.org",
    'UNICHAIN':  "https://unichain.drpc.org",
    'MODE': "https://mode.drpc.org"
}

# Основная асинхронная функция
async def get_tx_counts_all_chains(address: str, proxies: list[str]) -> dict[str, int | str]:
    results = {}

    for chain, rpc in NETWORKS.items():
        proxy = random.choice(proxies)
        try:
            connector = aiohttp.TCPConnector(ssl=False)
            proxy_session = aiohttp.ClientSession(connector=connector)
            provider = AsyncHTTPProvider(rpc, session=proxy_session, request_kwargs={"proxy": proxy})

            w3 = AsyncWeb3(provider)

            if not w3.is_address(address):
                results[chain] = "❌ invalid address"
                await proxy_session.close()
                continue

            tx_count = await w3.eth.get_transaction_count(address)
            results[chain] = tx_count
        except Exception as e:
            results[chain] = f"⚠️ error: {str(e)}"
        finally:
            await proxy_session.close()

    return results

# Пример запуска
# import asyncio
# proxies = load_proxies("proxy.txt")
# result = asyncio.run(get_tx_counts_all_chains("0xYourAddressHere", proxies))
# print(result)