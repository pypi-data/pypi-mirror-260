import math

from eth_account import Account, hdaccount
from eth_account.signers.local import LocalAccount
from eth_utils import ValidationError


def for_words(words='') -> LocalAccount:
    """
    用助记词导入
    :param words: 助记词
    :return:
    """
    if words == '':
        words = hdaccount.generate_mnemonic(12, 'english')
    else:
        if not hdaccount.Mnemonic.is_mnemonic_valid(words):
            raise ValidationError(
                f"Provided words: '{words}', are not a valid BIP39 mnemonic phrase!"
            )
    seed = hdaccount.seed_from_mnemonic(words, '')
    key = hdaccount.key_from_seed(seed, hdaccount.ETHEREUM_DEFAULT_PATH)
    return Account.from_key(key.hex())


def for_keys(key) -> LocalAccount:
    """
    用私钥导入
    :param key: 私钥
    :return:
    """
    return Account.from_key(key.hex())


def create():
    """
    创建钱包
    :return: account account.address account.key.hex()
    """
    return Account.create()


def format_value(amount, pre):
    """
    转换精度
    :param amount: 金额
    :param pre: 精度
    :return:
    """
    return int(amount * math.pow(10, pre))