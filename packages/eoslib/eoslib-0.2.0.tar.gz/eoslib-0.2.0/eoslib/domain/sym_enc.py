from metis_crypto import jwk, jwe
from metis_crypto.common import json_encode

from pymonad.maybe import Maybe

from eoslib.util import encoding_helpers, monad
from eoslib import domain


def sym_encrypt(data: str) -> monad.EitherMonad[str]:
    key_result = _build_enc_key()
    if key_result.is_left():
        return key_result
    return monad.Right(encoding_helpers.decode(key_result.value.compiled_key.encrypt(encoding_helpers.encode(data))))


def sym_decrypt(cypher_text: str) -> monad.EitherMonad[str]:
    key_result = _build_enc_key()
    if key_result.is_left():
        return key_result

    return monad.Right(
        encoding_helpers.decode(key_result.value.compiled_key.decrypt(encoding_helpers.encode(cypher_text))))


def jwe_encrypt(data: str) -> monad.EitherMonad[str]:
    """
    Generates a JWE encoded str
    The advantage of JWE is that the json encoded str contains the KID (and ALG/ENC) allowing cypher text to be stored
    across key rotations.

    Use this technique for long-lived cypher text, such as client secrets.
    """
    key_result = _build_enc_jwk()
    if key_result.is_left():
        return key_result
    jwetoken = jwe.JWE(encoding_helpers.encode(data),
                       json_encode({"kid": key_result.value.compiled_key.kid,
                                    "alg": "A256KW",
                                    "enc": "A256CBC-HS512"}))
    jwetoken.add_recipient(key_result.value.compiled_key)

    return monad.Right(jwetoken.serialize())


def jwe_decrypt(cypher_text) -> monad.EitherMonad[str]:
    jwetoken = jwe.JWE()
    jwetoken.deserialize(cypher_text)
    key_result = _build_enc_jwk_by_kid(jwetoken.jose_header['kid'])
    if key_result.is_left():
        return key_result

    jwetoken.decrypt(key_result.value.compiled_key)
    return monad.Right(encoding_helpers.decode(jwetoken.payload))


#
# Helpers
#
def _build_enc_key() -> Maybe[domain.CompiledKey]:
    return domain.build_key_by_use(domain.KeyUse.ENC)


def _build_enc_jwk() -> Maybe[domain.CompiledKey]:
    return domain.build_key_by_use(domain.KeyUse.JWTENC)


def _build_enc_jwk_by_kid(kid: str) -> monad.EitherMonad[jwk.JWK]:
    return domain.build_key_by_kid(kid)
    # return domain.get_key_by_kid(kid)
