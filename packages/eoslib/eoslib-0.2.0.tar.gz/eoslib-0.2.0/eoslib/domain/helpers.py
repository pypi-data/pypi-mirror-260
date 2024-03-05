from __future__ import annotations
from typing import Union, Optional, Callable
import uuid

from pymonad.maybe import Maybe, Just, Nothing
from metis_crypto import jwk

from eoslib import domain
from eoslib.util import monad, error, state_machine as sm

def assign_kid():
    return str(uuid.uuid4())


def get_key_by_use(use: domain.KeyUse,
                   decrypter: Optional[Callable] = None) -> monad.EitherMonad[domain.Key]:
    """
    gets the key from the keystore and decrypts it.
    Only gets the Active Key
    :param use:
    :return:
    """
    maybe_stored_key: Maybe[domain.Key] = domain.KEYSTORE.get_key_by_use(use)

    if maybe_stored_key.is_nothing():
        return monad.Left(None)
    if not decrypter:
        return monad.Right(maybe_stored_key.value)
    return decrypter(maybe_stored_key.value)



def get_key_by_kid(kid: domain.Kid,
                   decrypter: Optional[Callable] = None) -> Maybe[domain.Key]:
    """
    gets the key from the keystore and decrypts it.
    Only gets the Active Key
    :param use:
    :return:
    """
    maybe_stored_key: Maybe[domain.Key] = domain.KEYSTORE.get_key_by_kid(kid)

    if maybe_stored_key.is_nothing():
        return maybe_stored_key
    if not decrypter:
        return maybe_stored_key
    # That's a Functor!!!
    return maybe_stored_key.map(decrypter).value


def key_state_transition(from_state: Optional[str], with_transition: str) -> monad.EitherMonad[str]:
    return sm.transition(state_map=domain.key_state_map(),
                         from_state=from_state,
                         with_transition=with_transition)
