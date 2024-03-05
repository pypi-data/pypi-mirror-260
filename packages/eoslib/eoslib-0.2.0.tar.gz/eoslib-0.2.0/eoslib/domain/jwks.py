from __future__ import annotations
from typing import Callable, Tuple, Optional
import json

from pymonad.maybe import Maybe, Just, Nothing
from metis_crypto import jwk

from eoslib import domain
from eoslib.util import monad, error


class JwksEnvCache(domain.KeyCacherProtocol):

    def __init__(self,
                 writer_fn: Callable,
                 reader_fn: Callable,
                 formatter: Callable,
                 builder: Callable,
                 use: domain.KeyUse):
        self.writer_fn = writer_fn
        self.reader_fn = reader_fn
        self.formatter = formatter
        self.use = use
        self.builder = builder

    def key_use(self):
        return self.use

    def read(self) -> domain.AddableExportableKeyTuple:
        return True, None, self.reader_builder(self.reader_fn())

    def write(self, **args) -> domain.Key:
        return self._writer(self.formatter(**args))

    def write_without_env_mutation(self, **args):
        self._writer(self.formatter(**args), mutate_env=False)

    def _writer(self, formatted_key, mutate_env: bool = True):
        _result = self.writer_fn(self._paramater_key(), mutate_env)(formatted_key.serialise_as_json())
        return formatted_key

    def reader_builder(self, val: Optional[str]) -> Maybe[dict]:
        if not val:
            return Nothing
        key: dict = json.loads(val)
        return Just(self.formatter(**key))

    def _paramater_key(self):
        return self.use.name

def get_jwks():
    maybe_jwks = domain.build_key_by_use(domain.KeyUse.JWKS)
    if maybe_jwks.is_left():
        return maybe_jwks
    return monad.Right(maybe_jwks.value.compiled_key)


def create_jwks():
    kid = domain.assign_kid()
    use = domain.KeyUse.JWKS
    state_result = domain.key_state_transition(from_state=None, with_transition='rotate')
    if state_result.is_left():
        return state_result

    existing_key_result = domain.get_key_by_use(use)

    domain.KEYSTORE.add_key(key_generation_fn=create_exportable_jwks(kid),
                            kid=kid,
                            alg='JWKS',
                            use=domain.KeyUse.JWKS,
                            state=state_result.value)
    if existing_key_result.is_right():
        domain.revoke_previous_key(existing_key_result)
    return monad.Right(kid)


def write_jwks_to_parameter_store_location(location_uri: str):
    jwks_result = domain.build_key_by_use(domain.KeyUse.JWKS)
    if jwks_result.is_left():
        return jwks_result
    jwks = json.dumps(jwks_result.value.compiled_key)
    return parameter_store.writer(location_uri, mutate_env=False, value_type=parameter_store.String)(jwks)


def create_exportable_jwks(kid) -> Callable:
    def key_generator_fn():
        return _jwks_generator(kid, domain.KeyUse.JWKS)

    return key_generator_fn


def _jwks_generator(kid, use) -> domain.AddableExportableKeyTuple:
    result = _create_jwks_from_signing_keys(kid, use)
    # This is called from KeyStore, and the False means not from Cache
    if result.is_right():
        kek_kid, _kid, cyphertext = result.value
        return False, kek_kid, Just(cyphertext)
    return False, None, Nothing


def _create_jwks_from_signing_keys(kid, use) -> monad.EitherMonad[domain.ExportableKeyTuple]:
    result: monad.EitherMonad[domain.EncryptedKey] = (_key_set() >>
                                                      _to_json >>
                                                      domain.kek_encrypt)
    if result.is_right():
        kek_kid, cyphertext = result.value
        return monad.Right((kek_kid, kid, cyphertext))
    return result


def _key_set():
    all_keys_result = domain.get_all_keys_by_use(domain.KeyUse.SIG,
                                                 decrypter_fn=domain.decrypter,
                                                 in_states=['active', 'depreciated'])
    if all_keys_result.is_left():
        return all_keys_result
    exported_jwks = list(map(_exporter, all_keys_result.value))
    key_set = {
        'keys': list(map(lambda either_jwks: either_jwks.lift(), exported_jwks))
    }
    return monad.Right(key_set)

def create_jwks_from_jwks(jwks):
    exported_jwks = list(map(_exporter, jwks))
    key_set = {
        'keys': list(map(lambda either_jwks: either_jwks.lift(), exported_jwks))
    }
    return monad.Right(key_set)


def _exporter(sig_key_result: monad.EitherMonad[jwk.JWK]) -> monad.EitherMonad[dict]:
    return sig_key_result.map(_export_public_jwk)


def _to_json(key_set) -> monad.EitherMonad[str]:
    return monad.Right(json.dumps(key_set))


def _export_public_jwk(jwk):
    return jwk.export_public(as_dict=True)


def decrypter(stored_key: domain.Key) -> monad.EitherMonad:
    return decrypt_jwks(stored_key.cyphertext)


def decrypt_stored_jwks(key: domain.Key) -> domain.CompiledKey:
    """
    Called as the builder from KeyStore.  Gets a keystore dict, and invokes the
    decrypter with the cyphertext
    :param key:
    :return:
    """
    return domain.CompiledKey(key=key, compiled_key=decrypt_jwks(key.cyphertext).value)


def decrypt_jwks(encrypted_serialised_jwks: str) -> monad.EitherMonad[dict]:
    result = (monad.Right(encrypted_serialised_jwks) >>
              domain.kek_decrypt >>
              _from_json)
    return result


@monad.Try(error_cls=error.JWKSError)
def _from_json(json_jwks: str) -> monad.EitherMonad[dict]:
    return json.loads(json_jwks)
