from __future__ import annotations
from typing import Tuple, List, Callable, Optional, Union, Any
import sys
from functools import partial

from cryptography.fernet import Fernet
from metis_crypto import jwk
from pymonad.maybe import Maybe, Just, Nothing

from eoslib.util import encoding_helpers, monad, error, state_machine as sm

from eoslib import domain


def rotate_symmetric_key(use: domain.KeyUse) -> monad.EitherMonad[domain.Kid]:
    kid = domain.assign_kid()

    existing_key_result = domain.get_key_by_use(use, decrypter=None)

    state_result = domain.key_state_transition(from_state=None, with_transition='rotate')

    domain.KEYSTORE.add_key(key_generation_fn=create_exportable_enc_key(kid,
                                                                        create_exportable_symmetric_key),
                            kid=kid,
                            alg='ASE-CBC-128-HMAC-SHA256',
                            use=use,
                            state=state_result.value)

    if existing_key_result.is_right():
        domain.revoke_previous_key(existing_key_result)

    return monad.Right(kid)


def rotate_symmetric_jwk(use: domain.KeyUse) -> monad.EitherMonad[domain.Kid]:
    kid: domain.Kid = domain.assign_kid()

    domain.KEYSTORE.add_key(key_generation_fn=create_exportable_enc_key(kid,
                                                                        create_exportable_symmetric_jwk),
                            kid=kid,
                            alg='oct',
                            use=use,
                            state='active')
    return monad.Right(kid)


def build_key_by_use(use: domain.KeyUse) -> Maybe[Any]:
    return domain.KEYSTORE.build(use=use)


def build_key_by_kid(kid: domain.Kid) -> Maybe[Any]:
    return domain.KEYSTORE.build(kid=kid)


def get_all_keys_by_use(use: domain.KeyUse,
                        decrypter_fn: Optional[Callable] = None,
                        in_states: List[str] = None) -> monad.EitherMonad[List[jwk.JWK]]:
    """
    gets the key from the keystore and decrypts it.
    :param use:
    :return:
    """
    maybe_stored_keys = domain.KEYSTORE.get_all_keys_by_use(use, in_states)
    if maybe_stored_keys.is_nothing():
        return monad.Left(error.KeyStoreError(f"failure to get key with use {use.name}"))
    if not decrypter_fn:
        return monad.Right(maybe_stored_keys.value)
    return monad.Right(list(map(decrypter_fn, maybe_stored_keys.value)))


def get_all_keys(decrypter_fn: Optional[Callable] = None,
                 in_states: List[str] = None) -> monad.EitherMonad[List[jwk.JWK]]:
    """
    gets all the keys.
    :param use:
    :return:
    """
    stored_keys = domain.KEYSTORE.get_all_keys(in_states)
    if not decrypter_fn:
        return monad.Right(stored_keys)
    return monad.Right(list(map(decrypter_fn, maybe_stored_keys.value)))


def decrypter(stored_key: domain.Key) -> monad.EitherMonad:
    return getattr(sys.modules[__name__], f"decrypt_{stored_key.use.value}")(stored_key.cyphertext)


def decrypt_sig(cyphertext):
    return decrypt_public_key_pair(cyphertext)


def decrypt_enc(cyphertext):
    return decrypt_sym_key(cyphertext)


def decrypt_kek(cyphertext):
    """
    The kek is not encrypted, so just return the cyphertext
    :param cyphertext:
    :return:
    """
    return monad.Right(cyphertext)


def decrypt_jwtenc(cyphertext):
    return decrypt_sym_jwk(cyphertext)

def decrypt_jwks(cyphertext):
    return domain.decrypt_jwks(cyphertext)



def get_public_key_pair_by_kid(kid) -> monad.EitherMonad[jwk.JWK]:
    maybe_stored_key: Maybe[domain.Key] = domain.KEYSTORE.get_key_by_kid(kid)
    if maybe_stored_key.is_nothing():
        return monad.Left(error.KeyStoreError(f"No Key with kid {kid} found"))
    return decrypt_public_key_pair(maybe_stored_key.value.cyphertext)


def decrypt_stored_sig(key: domain.Key) -> domain.CompiledKey:
    """
    Called as the builder from KeyStore.  Gets a keystore dict, and envokes the
    decrypter with the cyphertext
    :param key:
    :return:
    """
    return domain.CompiledKey(key=key,
                              compiled_key=(decrypt_public_key_pair(key.cyphertext, kek_kid=key.encrypting_kid).value))


def decrypt_public_key_pair(encrypted_serialised_pair: str,
                            kek_kid: Optional[str] = None) -> monad.EitherMonad[jwk.JWK]:
    result = (monad.Right(encrypted_serialised_pair) >>
              partial(domain.kek_decrypt, encrypting_kid=kek_kid) >>
              domain.load_pair_from_json)
    return result


def decrypt_enc_key(key: domain.Key) -> domain.CompiledKey:
    return domain.CompiledKey(key=key, compiled_key=decrypt_sym_key(key.cyphertext).value)


def decrypt_sym_key(serialised_key) -> monad.EitherMonad[Fernet]:
    result = (monad.Right(serialised_key) >>
              domain.kek_decrypt >>
              to_fernet_key)
    return result


def decrypt_jwt_enc_key(key: domain.Key) -> domain.CompiledKey:
    return domain.CompiledKey(key=key, compiled_key=decrypt_sym_jwk(key.cyphertext).value)


def decrypt_sym_jwk(serialised_jwk) -> monad.EitherMonad[jwk.JWK]:
    result = (monad.Right(serialised_jwk) >>
              domain.kek_decrypt >>
              to_jwk)
    return result


def create_exportable_enc_key(kid, generation_fn: Callable):
    def key_generator_fn():
        return enc_generator(generation_fn, kid, domain.KeyUse.SIG)

    return key_generator_fn


def enc_generator(generation_fn, kid: str, use: domain.KeyUse) -> domain.AddableExportableKeyTuple:
    result = generation_fn(kid, use)
    # This is called from KeyStore, and the False means not from Cache
    if result.is_right():
        kek_kid, _kid, cyphertext = result.value
        return False, kek_kid, Just(cyphertext)
    return False, None, Nothing


def create_exportable_symmetric_key(kid: str, use: domain.KeyUse) -> monad.EitherMonad[Tuple[str, str]]:
    key_result: monad.EitherMonad[domain.EncryptedKey] = (monad.Right(kid) >>
                                                          partial(create_sym_key, True) >>
                                                          domain.kek_encrypt)
    if key_result.is_right():
        kek_kid, cyphertext = key_result.value
        return monad.Right((kek_kid, kid, cyphertext))
    return key_result


def create_exportable_symmetric_jwk(kid: str, use: domain.KeyUse) -> monad.EitherMonad[Tuple[str, str]]:
    result: monad.EitherMonad[domain.EncryptedKey] = (monad.Right(kid) >>
                                                      create_sym_jwk >>
                                                      jwk_export >>
                                                      domain.kek_encrypt)
    if result.is_right():
        kek_kid, cyphertext = result.value
        return monad.Right((kek_kid, kid, cyphertext))

    return result


#
# Helpers
#


@monad.Try(error_cls=error.SymKeyError)
def to_fernet_key(key):
    return Fernet(encoding_helpers.encode(key))


@monad.Try(error_cls=error.JWTError)
def to_jwk(key):
    return jwk.JWK().from_json(key)


def create_sym_key(as_decoded: bool, _kid) -> monad.EitherMonad[str]:
    if as_decoded:
        return monad.Right(encoding_helpers.decode(Fernet.generate_key()))
    return monad.Right(Fernet.generate_key())


def create_sym_jwk(kid):
    return monad.Right(jwk.JWK.generate(kid=kid, kty='oct', size=256))


@monad.Try(error_cls=error.JWKSError)
def jwk_export(key: jwk.JWK) -> monad.EitherMonad[str]:
    return key.export()
