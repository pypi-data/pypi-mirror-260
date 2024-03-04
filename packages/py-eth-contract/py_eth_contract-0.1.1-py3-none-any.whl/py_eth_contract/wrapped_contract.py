
from typing import List, Optional

from web3 import Web3
from web3.eth import Eth

from web3.contract import ContractEvents, ContractFunction, ContractFunctions, Contract as EthContract
from eth_account.signers.local import LocalAccount

from .contract_utils import method_signature
from .exceptions import NoAccountException


class WrappedContract:

    def __init__(
        self,
        eth: Eth,
        address: str,
        abi: List[dict],
        account: Optional[LocalAccount] = None
    ):
        self.__eth = eth
        self.__address = address
        self.__abi = abi

        self.__contract = eth.contract(
            address=Web3.to_checksum_address(address),
            abi=abi
        )

        self._account = account



    @property
    def eth(self) -> Eth:
        return self.__eth

    @property
    def address(self) -> str:
        return self.__address

    @property
    def abi(self) -> str:
        return self.__abi

    @property
    def contract(self) -> EthContract:
        return self.__contract

    @property
    def functions(self) -> ContractFunctions:
        return self.__contract.functions

    @property
    def events(self) -> ContractEvents:
        return self.__contract.events


    @staticmethod
    def method_signature(method: ContractFunction) -> str:
        return method_signature(method)

    def raw_transaction(
        self,
        function: ContractFunction,
        wei: Optional[int] = None,
        gas: Optional[int] = None,
        gas_price: Optional[int] = None,
        max_fee_per_gas: Optional[int] = None,
        max_priority_fee_per_gas: Optional[int] = None,
        account: Optional[LocalAccount] = None
    ):
        account = account or self._account

        if not account:
            raise NoAccountException(
                contract_address=function.address,
                function_name=function.fn_name
            )

        transaction_data = {
            'nonce': self.eth.getTransactionCount(account.address),
            'gas': gas,
            'gasPrice': gas_price,
            'maxFeePerGas': max_fee_per_gas,
            'maxPriorityFeePerGas': max_priority_fee_per_gas,
            'value': wei
        }

        txn = function.buildTransaction({k:v for k, v in transaction_data.items() if v is not None})

        return account.sign_transaction(txn).rawTransaction

    def send_transaction(
        self,
        function: ContractFunction,
        wei: Optional[int] = None,
        gas: Optional[int] = None,
        gas_price: Optional[int] = None,
        max_fee_per_gas: Optional[int] = None,
        max_priority_fee_per_gas: Optional[int] = None,
        account: Optional[LocalAccount] = None
    ) -> str:
        return self.eth.sendRawTransaction(
            self.raw_transaction(
                function=function,
                wei=wei,
                gas=gas,
                gas_price=gas_price,
                max_fee_per_gas=max_fee_per_gas,
                max_priority_fee_per_gas=max_priority_fee_per_gas,
                account=account
            )
        ).hex()

