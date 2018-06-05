import argparse
import logging

from multicrypto.address import translate_private_key, validate_base58, \
    get_private_key_from_wif_format, convert_private_key_to_address
from multicrypto.coins import coins, validate_coin_symbol

logger = logging.getLogger(__name__)


def get_args():
    parser = argparse.ArgumentParser(description='Translates private key between different coins. '
                                                 'Without specifying output symbol it will return integer '
                                                 'value of the private key')
    parser.add_argument('-p', '--private_key', type=str, required=True,
                        help='Private key which we want to translate')
    parser.add_argument('-o', '--output_symbol', type=str, required=False, default='',
                        help='Symbol of the coin for which we want to know corresponding '
                             'translated private key')
    parser.add_argument('-f', '--file', type=str, required=False, default=None,
                        help='Store script output in the provided file')
    return parser.parse_args()


def translate(args):
    output_coin_symbol = args.output_symbol.upper()
    wif_private_key = args.private_key
    file_name = args.file

    if file_name:
        file_handler = logging.FileHandler(file_name)
        logger.addHandler(file_handler)

    if not output_coin_symbol:
        translated_private_key = get_private_key_from_wif_format(wif_private_key)
        return translated_private_key, ''

    try:
        validate_coin_symbol(output_coin_symbol)
        validate_base58(wif_private_key)
    except Exception as e:
        logger.error(e)
        return '', ''

    output_private_key_prefix_bytes = coins[output_coin_symbol]['secret_prefix_bytes']
    output_address_prefix_bytes = coins[output_coin_symbol]['address_prefix_bytes']
    translated_private_key = translate_private_key(wif_private_key, output_private_key_prefix_bytes)
    private_key, compressed = get_private_key_from_wif_format(wif_private_key)
    address = convert_private_key_to_address(private_key, output_address_prefix_bytes, compressed)
    return translated_private_key, address


def main():
    args = get_args()
    translated_private_key, address = translate(args)
    print('{} private key: {}, address: {}'.format(
        args.output_symbol, translated_private_key, address))


if __name__ == '__main__':
    main()
