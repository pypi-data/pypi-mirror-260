from __future__ import annotations
from typing import Callable, Dict, List, Union, Tuple, Optional, Protocol
from dataclasses import dataclass
from functools import partial
from collections import defaultdict
import json

from pymonad.maybe import Maybe, Just, Nothing

from eoslib import domain
from eoslib.util import fn, monad, error


@dataclass
class Key:
    use: Union[domain.KeyUse, str]
    cyphertext: str
    kid: Optional[str] = None
    alg: Optional[str] = None
    encrypting_kid: Optional[str] = None
    state: Optional[str] = None

    def is_active(self):
        return self.state == 'active'

    def is_depreciated(self):
        return self.state == 'depreciated'

    def is_in_states(self, in_states: List[str]):
        return self.state in in_states

    def serialise_as_json(self):
        return json.dumps({
            'kid': self.kid,
            'alg': self.alg,
            'cyphertext': self.cyphertext,
            'encrypting_kid': self.encrypting_kid,
            'state': self.state,
            'use': self.use.value
        })


class GenericKeyCacher(domain.KeyCacherProtocol):

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

    def read(self) -> Tuple[bool, Maybe[str]]:
        return True, None, self.reader_builder(self.reader_fn())

    def key_use(self):
        return self.use

    def write_without_env_mutation(self, **args):
        self._writer(self.formatter(**args), mutate_env=False)

    def write(self, **args) -> Key:
        return self._writer(self.formatter(**args))

    def _writer(self, formatted_key, mutate_env: bool = True):
        result = self.writer_fn(self._paramater_key(), mutate_env)(formatted_key.serialise_as_json())
        return formatted_key

    def reader_builder(self, val: Optional[str]) -> Maybe[dict]:
        if not val:
            return Nothing
        key: dict = json.loads(val)
        return Just(self.formatter(**key))

    def _paramater_key(self):
        return self.use.name


def base_key_formatter(cyphertext, use: Union[str, domain.KeyUse], kid, alg, state, encrypting_kid) -> Key:
    return Key(kid=kid,
               cyphertext=cyphertext,
               alg=alg,
               use=use if isinstance(use, domain.KeyUse) else domain.KeyUse(use),
               encrypting_kid=encrypting_kid,
               state=state)


def get_active(keys: List[Key]) -> Maybe[Key]:
    """
    Return only the active key
    :param self:
    :param keys:
    :return:
    """
    key = fn.find(lambda k: k.is_active(), keys)
    if not key:
        return Nothing
    return Just(key)


def get_keys_in_state(in_states, keys: List[Key]) -> Maybe[List[Key]]:
    return Just(list(fn.select(lambda key: key.is_in_states(in_states), keys)))


class IdentityWriter:
    def writer(self, key: str, mutate_env: bool = True, value_type: str = "SecureString") -> Callable:
        """
        Implements a writer protocol for a KeyStore Cacher.  Returns a writer fn which will persist the key
        in ParameterStore.  Takes the key, a flag indicating whether to mutate the env, and a value type
        and returns a partial applied fn with will take the value to be persisted.
        :param key:
        :param mutate_env:
        :param value_type:
        :return:
        """
        return partial(self.write, key, mutate_env, value_type)

    def write(self, key, mutate_env, value_type, value):
        pass


class KeyStore:
    kids = {}
    uses = defaultdict(list)
    key_cachers = {}

    def configure_key_cacher_for_use(self, cacher: domain.KeyCacherProtocol):
        self.key_cachers[cacher.key_use()] = cacher
        return self

    def clear(self):
        self.uses = defaultdict(list)
        self.kids = {}

    def add_key(self,
                key_generation_fn: Callable,
                use: domain.KeyUse,
                kid: str = None,
                alg: str = None,
                state: str = None):
        from_cache, kek_kid, maybe_key = key_generation_fn()
        if maybe_key.is_nothing():
            return self
        if not from_cache:
            formatted_key: Key = self.key_cacher_for(use).write(cyphertext=maybe_key.value,
                                                                use=use,
                                                                kid=kid,
                                                                encrypting_kid=kek_kid,
                                                                alg=alg,
                                                                state=state)
        else:
            formatted_key: Key = maybe_key.value
            kid = formatted_key.kid
        self.track_key(kid, use, formatted_key)
        return self

    def track_key(self, kid, use, formatted_key):
        self.uses[use].append(formatted_key)
        if kid:
            self.kids[kid] = formatted_key


    def key_cacher_for(self, use):
        cacher = self.key_cachers.get(use)
        if not cacher:
            return IdentityWriter()
        return cacher

    def add_key_set(self, key_set):
        if not self.jwks_cache:
            return None
        self.jwks_cache.write(key_set)
        return self

    def build(self,
              use: Optional[domain.KeyUse] = None,
              kid: Optional[domain.Kid] = None,
              is_cache_initialised: bool = False) -> monad.EitherMonad[domain.CompiledKey]:
        """
        Takes a KID or a Use.  Gets the key, called the configured key builder
        which returns a CompiledKey
        :param use:
        :param kid:
        :param is_cache_initialised:
        :return:
        """
        maybe_key = self.get_key_by_use(use) if use else self.get_key_by_kid(kid)
        if maybe_key.is_just():
            return monad.Right(maybe_key.value).map(self.key_cacher_for(use if use else maybe_key.value.use).builder)
        if is_cache_initialised:  # it's initialised but there is no key available
            return monad.Left(error.KeyStoreError(f"Initialised but no key available for {use.name}"))
        # Read through to the cache
        if not use:
            return monad.Left(error.KeyStoreError("Can't initialise without a USE"))
        self.add_key(self.key_cacher_for(use).read, use)
        return self.build(use, is_cache_initialised=True)

    def change_key_state(self, kid: domain.Kid, new_state: str):
        maybe_key = self.get_key_by_kid(kid)
        if maybe_key.is_nothing():
            return self
        maybe_key.value.state = new_state
        maybe_key.map(self.write_update)
        return self

    def write_update(self, key: Key):
        self.key_cacher_for(key.use).write_without_env_mutation(cyphertext=key.cyphertext,
                                                                use=key.use,
                                                                kid=key.kid,
                                                                alg=key.alg,
                                                                encrypting_kid=key.encrypting_kid,
                                                                state=key.state)
        return self

    def get_key_by_kid(self, kid):
        key = self.kids.get(kid, None)
        if not key:
            return Nothing
        return Just(key)

    def get_key_by_use(self,
                       use,
                       extract_fn: Callable = get_active) -> Union[List[Maybe[dict]], Maybe[dict]]:
        keys = self.uses.get(use, None)
        if not keys:
            return Nothing

        return extract_fn(keys)

    def get_all_keys_by_use(self, use, in_states: List[str] = None) -> Maybe[List[Dict]]:
        extract_fn = (lambda keys: Just(keys)) if not in_states else partial(get_keys_in_state, in_states)
        return self.get_key_by_use(use, extract_fn)

    def get_all_keys(self, in_states: List[str] = None) -> Maybe[List[Dict]]:
        return [key for key in self.kids.values()]


KEYSTORE = KeyStore()
# (KEYSTORE.key_cacher_for_use(GenericKeyCacher(formatter=base_key_formatter,
#                                               builder=domain.build_kek,
#                                               use=domain.KeyUse.KEK))
#  .key_cacher_for_use(GenericKeyCacher(formatter=base_key_formatter,
#                                       builder=domain.decrypt_stored_sig,
#                                       use=domain.KeyUse.SIG))
#  .key_cacher_for_use(GenericKeyCacher(formatter=base_key_formatter,
#                                       builder=domain.decrypt_enc_key,
#                                       use=domain.KeyUse.ENC))
#  .key_cacher_for_use(GenericKeyCacher(formatter=base_key_formatter,
#                                       builder=domain.decrypt_jwt_enc_key,
#                                       use=domain.KeyUse.JWTENC))
#  .key_cacher_for_use(domain.JwksEnvCache(formatter=base_key_formatter,
#                                          builder=domain.decrypt_stored_jwks,
#                                          use=domain.KeyUse.JWKS))
#
#  )
