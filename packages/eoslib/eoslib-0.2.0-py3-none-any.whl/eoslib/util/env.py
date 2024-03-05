import os
from typing import List, Tuple

from eoslib.util import monad


# Global Object
class Env:
    env = os.environ.get('ENVIRONMENT', default=None)

    # region_name = os.environ.get('REGION_NAME', default='ap-southeast-2')

    expected_envs = []

    # @staticmethod
    # def parameter_store_path():
    #     return os.environ.get('PARAMETER_STORE_PATH', default=None)
    #
    #
    # @staticmethod
    # def dynamodb_table():
    #     # When in test the table might not have been setup from the env
    #     if Env.test() and os.environ.get('DYNAMODB_TABLE_NAME', None) is None:
    #         os.environ['DYNAMODB_TABLE_NAME'] = 'selene.refarch.io'
    #
    #     return os.environ.get('DYNAMODB_TABLE_NAME', default=None)

    @staticmethod
    def KEK():
        return os.environ.get('KEK', default=None)

    @staticmethod
    def SIG():
        return os.environ.get('SIG', default=None)

    @staticmethod
    def JWKS():
        return os.environ.get('JWKS', default=None)

    @staticmethod
    def ENC():
        return os.environ.get('ENC', default=None)

    @staticmethod
    def JWTENC():
        return os.environ.get('JWTENC', default=None)



    @staticmethod
    def HOME():
        return os.environ.get('HOME', default=None)


    @staticmethod
    def development():
        return Env.env == "development"

    @staticmethod
    def test():
        return Env.env == "test"

    @staticmethod
    def production():
        return not (Env.development() or Env.test())

    @staticmethod
    def expected_set():
        return all(getattr(Env, var)() for var in Env.expected_envs)

    def set_env_var_with_value(self, name: str, value: str) -> Tuple[str, str, str]:
        """
        Sets an ENV variable from a key/value pair
        """
        os.environ[name] = value
        return ('ok', name, value)


def set_env(parameters: List[dict]):
    return monad.Right(list(map(set_env_var, parameters['Parameters'])))


def set_env_var_with_parameter(parameter: dict) -> Tuple:
    """
    Sets an ENV variable from the parameter store data structure
    """
    name = parameter['Name'].split("/")[-1]
    os.environ[name] = parameter['Value']
    return monad.Right(('ok', name, parameter['Value']))


def set_env_var_with_value(name: str, value: str) -> Tuple[str, str, str]:
    """
    Sets an ENV variable from a key/value pair
    """
    os.environ[name] = value
    return ('ok', name, value)
