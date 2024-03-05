from __future__ import annotations
from typing import Tuple, List, Callable, Optional, Union
from functools import partial

from metis_crypto import jwk
from pymonad.maybe import Maybe, Just, Nothing

from eoslib.util import monad

from eoslib import domain


def rotate_public_key_pair(use: domain.KeyUse = None,
                           gracefully: bool = True,
                           export_jwks: bool = False):
    kid = domain.assign_kid()
    state_result = domain.key_state_transition(from_state=None, with_transition='rotate')
    if state_result.is_left():
        return state_result

    existing_key_result = domain.get_key_by_use(use)

    domain.KEYSTORE.add_key(key_generation_fn=create_exportable_sig_key(kid),
                            kid=kid,
                            alg='RSA',
                            use=domain.KeyUse.SIG,
                            state=state_result.value)

    if existing_key_result.is_right():
        domain.revoke_previous_key(existing_key_result, gracefully)

    if not export_jwks:
        return monad.Right(kid)
    domain.create_jwks()

    return monad.Right(kid)


def create_exportable_sig_key(kid) -> Callable:
    def key_generator_fn():
        return sig_generator(kid, domain.KeyUse.SIG)

    return key_generator_fn


def sig_generator(kid, use) -> domain.AddableExportableKeyTuple:
    result = create_exportable_public_key_pair(kid, use)
    # This is called from KeyStore, and the False means not from Cache
    if result.is_right():
        kek_kid, _kid, cyphertext = result.value
        return False, kek_kid, Just(cyphertext)
    return False, None, Nothing


def create_exportable_public_key_pair(kid: str = None,
                                      use: domain.KeyUse = None) -> monad.EitherMonad[domain.ExportableKeyTuple]:
    kid = kid if kid else domain.assign_kid()
    result: monad.EitherMonad[domain.EncryptedKey] = (monad.Right(kid if kid else domain.assign_kid()) >>
                                                      partial(create_rsa_key_pair, use) >>
                                                      domain.export_pair_as_json >>
                                                      domain.kek_encrypt)
    if result.is_right():
        kek_kid, cyphertext = result.value
        return monad.Right((kek_kid, kid, cyphertext))
    return result


def create_rsa_key_pair(use, kid) -> monad.EitherMonad[jwk.JWK]:
    return domain.create_rsa_key_pair(kid=kid, use=use)
