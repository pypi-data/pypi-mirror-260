from web3 import Web3


class ContractApi(object):

    def __init__(self, chain_id, rpc_http, CONTRACT_ADDRESS=None, CONTRACT_ABI=None, ADDRESS=None, PRIVATE_KEY=None,
                 gas_num=None):
        self.CHAIN_ID = chain_id
        self.RPC = rpc_http
        self.web3 = Web3(Web3.HTTPProvider(rpc_http))
        self.CONTRACT_ADDRESS = CONTRACT_ADDRESS
        self.CONTRACT_ABI = CONTRACT_ABI
        self.GAS_NUM = gas_num
        self.ADDRESS = ADDRESS
        self.PRIVATE_KEY = PRIVATE_KEY

    def get_gas_limit(self, data, address):
        data['from'] = address
        limit = self.web3.eth.estimate_gas(data)
        limit = int(limit * (1 + 0.15))
        return limit

    def init_contract(self, contract_address=None):
        """
        初始化合约
        :param contract_address: 合约地址
        :return:
        """
        if contract_address:
            my_contract = self.web3.eth.contract(address=Web3.to_checksum_address(contract_address),
                                                 abi=self.CONTRACT_ABI)
        else:
            my_contract = self.web3.eth.contract(address=Web3.to_checksum_address(self.CONTRACT_ADDRESS),
                                                 abi=self.CONTRACT_ABI)
        return my_contract

    def get_erc_balance(self, address):
        """
        获取代币余额
        :param address: 地址
        :return:
        """
        return self.init_contract().functions.balanceOf(Web3.to_checksum_address(address)).call()

    def transfer_erc(self, to_address, amount, from_address=None, private_key=None, nonce=None):
        """
        代币转账
        :param to_address: 目的地址
        :param amount: 数量
        :param from_address: 转账地址
        :param private_key: 转账私钥
        :param nonce:
        :return:
        """
        if from_address is not None:
            self.ADDRESS = from_address
        if private_key is not None:
            self.PRIVATE_KEY = private_key
        if nonce is None:
            nonce = self.web3.eth.get_transaction_count(Web3.to_checksum_address(self.ADDRESS))
        gas_price = self.web3.eth.gas_price

        txn = self.init_contract().functions.transfer(Web3.to_checksum_address(to_address),
                                                      amount).buildTransaction({
            'chainId': self.CHAIN_ID,
            'gas': self.GAS_NUM,
            'gasPrice': gas_price + self.web3.to_wei('1', 'gwei'),
            'nonce': nonce,
        })
        try:
            txn['gas'] = self.get_gas_limit(txn, Web3.to_checksum_address(self.ADDRESS))
        except Exception:
            pass
        signed_txn = self.web3.eth.account.signTransaction(txn, private_key=self.PRIVATE_KEY)

        tmp = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_hash = self.web3.to_hex(tmp)
        return tx_hash

    def approve(self, address, amount):
        """
        代币授权
        :param address: 授权的地址
        :param amount: 数量
        :return:
        """
        gas_price = self.web3.eth.gas_price
        nonce = self.web3.eth.get_transaction_count(Web3.to_checksum_address(self.ADDRESS))
        txn = self.init_contract().functions.approve(Web3.to_checksum_address(address), amount).buildTransaction({
            'chainId': self.CHAIN_ID,
            'gas': self.GAS_NUM,
            'gasPrice': gas_price + self.web3.to_wei('1', 'gwei'),
            'nonce': nonce,
        })
        try:
            txn['gas'] = self.get_gas_limit(txn, Web3.to_checksum_address(self.ADDRESS))
        except Exception:
            pass
        signed_txn = self.web3.eth.account.signTransaction(txn, private_key=self.PRIVATE_KEY)

        tmp = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_hash = self.web3.to_hex(tmp)
        return tx_hash

    def allowance(self, owner, spender):
        """
        获取授权的数量
        :param owner: 目的地址
        :param spender: 目的合约地址
        :return:
        """
        return self.init_contract().functions.allowance(Web3.to_checksum_address(owner),
                                                        Web3.to_checksum_address(spender)).call()

    def decimals(self):
        """
        查询精度
        :return: 精度
        """
        return self.init_contract().functions.decimals().call()

    def total_supply(self):
        """
        查询供应量
        :return: 供应量
        """
        total_num = self.init_contract().functions.totalSupply().call()
        return total_num / pow(10, self.decimals())

    def symbol(self):
        """
        查询代币别名
        :return: 别名
        """
        try:
            return self.init_contract().functions.symbol().call()
        except Exception:
            return ''

    def name(self):
        """
        查询代币全称
        :return:
        """
        try:
            return self.init_contract().functions.name().call()
        except Exception:
            return ''