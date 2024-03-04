from __future__ import annotations
from typing import Union, Tuple
from cryptography.fernet import Fernet
import json

from pymonad.maybe import Maybe, Just, Nothing

from eoslib import domain
from eoslib.util import env, encoding_helpers, monad, error

"""
The KEK is the key used to enc all the other keys (public and symmetric) so that they can be stored in the Key store.
Dont use the KEK for anything but this purpose.


TODO: This key will come from AWS key management on initialisation.

For testing use the fixture "set_up_key_management" from tests.shared.key_management_helpers or call the setup directly using
tests.shared.key_management_helpers.set_up_key_management_env

"""


def rotate_kek(use: domain.KeyUse):
    kid = domain.assign_kid()
    state_result = domain.key_state_transition(from_state=None, with_transition='rotate')

    if state_result.is_left():
        return state_result

    existing_key_result = domain.get_key_by_use(use, decrypter=None)

    domain.KEYSTORE.add_key(key_generation_fn=create_kek,
                            kid=kid,
                            alg=None,
                            use=use,
                            state='active')

    # TODO: Version KEK
    # if existing_key_result.is_right():
    #     domain.revoke_previous_key(existing_key_result, _re_encrypt_keys_with_new_kek)

    return monad.Right(kid)


def build_kek(key: domain.Key) -> domain.CompiledKey:
    """
    Takes the key dict from the store and encodes it as a Fernet key.
    No decyrption is performed.
    :param key_dict:
    :return:
    """

    return domain.CompiledKey(key=key, compiled_key=Fernet(encoding_helpers.encode(key.cyphertext)))


def create_kek() -> Tuple[bool, Maybe[str]]:
    """
    Create a new kek.  The key is NOT from cache, so we return False
    :return:
    """
    return False, None, Just(encoding_helpers.decode(Fernet.generate_key()))


def kek_encrypt(data: str, as_str: bool = True) -> monad.EitherMonad[Tuple[domain.Kid, Union[bytes, str]]]:
    kek_result = kek(build=True)
    if kek_result.is_left():
        return monad.Left(error.KeyStoreError("No KEK initialised"))
    token = kek_result.value.compiled_key.encrypt(encoding_helpers.encode(data))

    if as_str:
        return monad.Right((kek_result.value.key.kid, encoding_helpers.decode(token)))
    return monad.Right((kek_result.value.key.kid, token))


def kek_decrypt(token: str, encrypting_kid: domain.Kid = None) -> monad.EitherMonad[str]:
    kek_result = kek(kek_kid=encrypting_kid, build=True)
    if kek_result.is_right():
        compiled_key = kek_result.value.compiled_key
    else:
        kek_result = kek(build=True)
        if kek_result.is_right():
            compiled_key = kek_result.value.compiled_key
        else:
            return monad.Left(error.KeyStoreError("No KEK initialised"))
    return monad.Right(encoding_helpers.decode(compiled_key.decrypt(encoding_helpers.encode(token))))


def kek(kek_kid: domain.Kid = None, build: bool = False) -> Maybe[domain.CompiledKey]:
    if kek_kid:
        return getattr(domain, f"{'build' if build else 'get'}_key_by_kid")(kid=kek_kid)
    return getattr(domain, f"{'build' if build else 'get'}_key_by_use")(use=domain.KeyUse.KEK)

