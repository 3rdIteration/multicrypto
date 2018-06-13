import argparse
import logging

from multicrypto.address import validate_address
from multicrypto.coins import coins, validate_coin_symbol
from multicrypto.network import send

logger = logging.getLogger(__name__)


def get_args():
    parser = argparse.ArgumentParser(description='Send cryptocurrency to specified address')
    parser.add_argument('-p', '--wif_private_key', type=str, required=True,
                        help='Private key in WIF format which funds will be used to send')
    parser.add_argument('-a', '--address', type=str, required=True,
                        help='Address to which we want to send')
    parser.add_argument('-c', '--coin_symbol', type=str, required=True, help='Symbol of the coin \
                        for which we want to make money transfer')
    parser.add_argument('-s', '--satoshis', type=str, required=True,
                        help='How many satoshis you want to send')
    parser.add_argument('-f', '--fee', type=str, required=False, default='1000',
                        help='Transaction fee')

    return parser.parse_args()


# TODO: validate wif private key
def send_crypto(args):
    coin_symbol = args.coin_symbol.upper()
    address = args.address
    wif_private_key = args.wif_private_key
    satoshis = int(args.satoshis)
    fee = int(args.fee)
    try:
        validate_coin_symbol(coin_symbol)
        validate_address(address, coin_symbol, is_script=False)
    except Exception as e:
        logger.error(e)
        return
    if not coins[coin_symbol].get('api'):
        logger.error('No api has been defined for coin {}'.format(coin_symbol))
    return send(coins[coin_symbol], wif_private_key, address, satoshis, fee)


def main():
    args = get_args()
    result = send_crypto(args)
    print(result)


if __name__ == '__main__':
    main()