from web3 import AsyncWeb3
from web3.providers.async_rpc import AsyncHTTPProvider


async def get_base_tx_count(address: str) -> int:
    # Инициализация Web3 с асинхронным HTTP-провайдером
    w3 = AsyncWeb3(AsyncHTTPProvider("https://base.llamarpc.com"))

    # Простая валидация адреса
    if not w3.is_address(address):
        raise ValueError("❌ Некорректный адрес Ethereum")

    # Получаем количество исходящих транзакций (nonce)
    tx_count = await w3.eth.get_transaction_count(address)
    return tx_count, address
