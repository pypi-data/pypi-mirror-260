
class NoAccountException(Exception):

    def __init__(
        self,
        contract_address: str,
        function_name: str
    ):
        self.__contract_address = contract_address
        self.__function_name = function_name

        super().__init__(f'No account to call function \'{function_name}\' of contract \'{contract_address}\' with.')



    @property
    def contract_address(self) -> str:
        return self.__contract_address

    @property
    def function_name(self) -> str:
        return self.__function_name



    def __reduce__(self):
        return (self.__class__, (self.__contract_address, self.__function_name))


# -------------------------------------------------------------------------------------------------------------------------------- #