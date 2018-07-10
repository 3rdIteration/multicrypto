import requests


def get_current_api_definition(coin):
    index = coin.get('current_api_index', 0)
    api_definition = coin['apis'][index]
    return api_definition


def api_send(coin, raw_transaction):
    api = get_current_api_definition(coin)
    send_url = '{}/tx/send'.format(api['url'])
    result = requests.post(send_url, json={'rawtx': raw_transaction})
    return result.text


def api_get_utxo(coin, address):
    api = get_current_api_definition(coin)
    address_url = '{}/addr/{}/utxo'.format(api['url'], address)
    result = requests.get(address_url)
    return result.json()


def api_get_last_block(coin):
    api = get_current_api_definition(coin)
    blocks_url = '{}/blocks?limit=1'.format(api['url'])
    result = requests.get(blocks_url)
    last_block = result.json()['blocks'][0]
    return last_block
