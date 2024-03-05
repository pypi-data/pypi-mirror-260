from web3 import Web3


class EthApi(object):
    """
    主币的基本方法
    """

    def __init__(self, chain_id, rpc_http, ADDRESS=None, PRIVATE_KEY=None):
        self.CHAIN_ID = chain_id
        self.RPC = rpc_http
        self.web3 = Web3(Web3.HTTPProvider(rpc_http))
        self.ADDRESS = ADDRESS
        self.PRIVATE_KEY = PRIVATE_KEY

    def transfer(self, to_address, amount, from_address=None, private_key=None, nonce=None):
        """
        主币转账
        :param to_address: 目的地址
        :param amount: 数量
        :param from_address: 转账的地址
        :param private_key: 私钥
        :param nonce:
        :return: 交易hash
        """
        if from_address is not None:
            self.ADDRESS = from_address
        if private_key is not None:
            self.PRIVATE_KEY = private_key
        if nonce is None:
            nonce = self.web3.eth.get_transaction_count(Web3.to_checksum_address(self.ADDRESS))
        gas_price = self.web3.eth.gas_price
        params = dict(
            gas=21000,
            gasPrice=gas_price,
            nonce=nonce,
            to=Web3.to_checksum_address(to_address),
            value=amount,
            chainId=self.CHAIN_ID,
        )

        signed_txn = self.web3.eth.account.signTransaction(params, self.PRIVATE_KEY)

        tmp = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_hash = self.web3.to_hex(tmp)
        return tx_hash

    def get_balance(self, address):
        """
        获取主币余额
        :param address: 地址
        :return: 余额
        """
        return self.web3.eth.get_balance(Web3.to_checksum_address(address))