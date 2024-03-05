from metis_crypto import jwk

from eoslib import domain
from eoslib.util import monad


def get_key_by_kid(kid) -> monad.EitherMonad[jwk.JWK]:
    return domain.get_public_key_pair_by_kid(kid)


def build_key_by_use(use: domain.KeyUse) -> monad.EitherMonad:
    return domain.build_key_by_use(use)


def get_key_by_use(use: domain.KeyUse) -> monad.EitherMonad[str]:
    """
    Gets a key which is already stored in the KeyStore.
    :param use:
    :return:
    """
    return domain.get_key_by_use(use)


def get_all_keys() -> monad.EitherMonad[str]:
    """
    All keys in all states
    :param use:
    :return:
    """
    return domain.get_all_keys()
