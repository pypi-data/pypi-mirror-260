from typing import Tuple, Union

from metis_crypto import jwk

from eoslib import domain
from eoslib.util import env, monad, error


# From CLI

def build_jwt_with_claims(**claims):
    return domain.generate_signed_jwt(domain.claims_builder(**claims))


def rotate_sig_key(use: domain.KeyUse = domain.KeyUse.SIG,
                   gracefully: bool = False,
                   export_jwks: bool = False):
    return domain.rotate_public_key_pair(use, gracefully, export_jwks)


def create_new_kek():
    return domain.rotate_kek(use=domain.KeyUse.KEK)


def get_current_jwks():
    return domain.get_key_by_use(use=domain.KeyUse.JWKS,
                                 decrypter=domain.decrypter)


def decode_jwt_and_validate(encoded_jwt: str,
                            expired_check: bool = False,
                            no_sig: bool = False) -> monad.Either[error.BaseError, dict]:
    result: monad.Either = domain.decode_jwt_and_validate(encoded_jwt, no_sig)
    if result.is_left() or not expired_check:
        return result
    if domain.is_jwt_claims_expired(result.value):
        return monad.Left('Expired')
    return result




# Internal


def rotate_public_key_pair(use: domain.KeyUse = domain.KeyUse.SIG,
                           gracefully: bool = False,
                           export_jwks: bool = False):
    result:monad.Either = domain.rotate_public_key_pair(use, gracefully, export_jwks)
    if result.is_right():
        return result
    return result


def rotate_symmetric_jwk():
    result:monad.Either = domain.rotate_symmetric_jwk(use=domain.KeyUse.JWTENC)
    if result.is_right():
        return result
    return result


def rotate_symmetric_key() -> monad.EitherMonad[Tuple[str, str]]:
    result:monad.Either = domain.rotate_symmetric_key(use=domain.KeyUse.ENC)
    if result.is_right():
        return result
    return result


def decrypt_sym_key(serialised_key) -> monad.EitherMonad:
    result:monad.Either = domain.decrypt_sym_key(serialised_key)
    if result.is_right():
        return result
    return result


def generate_signed_jwt(claims: dict):
    result:monad.Either = domain.generate_signed_jwt(claims)
    if result.is_right():
        return result
    return result


def decrypt_public_key_pair(serialised_pair) -> monad.EitherMonad[jwk.JWK]:
    return domain.decrypt_public_key_pair(serialised_pair)


def create_exportable_public_key_pair(use: domain.KeyUse = None) -> monad.EitherMonad[Tuple[str, str]]:
    pair_result = domain.create_exportable_public_key_pair(use=use)
    return pair_result


def create_rsa_key_pair(kid, use: domain.KeyUse = None):
    pair_result = domain.create_rsa_key_pair(kid, use)
    return pair_result


def export_pair_as_json(pair: jwk.JWK) -> str:
    export_pair_result = domain.export_pair_as_json(pair)
    return export_pair_result


def load_pair_from_json(json_pair: str) -> monad.EitherMonad[jwk.JWK]:
    loaded_pair_result = domain.load_pair_from_json(json_pair)
    return loaded_pair_result


def kek_encrypt(data: str, as_str: bool = True) -> monad.EitherMonad[Tuple[domain.Kid, Union[bytes, str]]]:
    result = domain.kek_encrypt(data, as_str)
    return result


def kek_decrypt(token: str) -> monad.EitherMonad[str]:
    result = domain.kek_decrypt(token)
    return result


def jwe_encrypt(data: str) -> monad.EitherMonad[str]:
    result = domain.jwe_encrypt(data)
    return result


def jwe_decrypt(cypher_text) -> monad.EitherMonad:
    result = domain.jwe_decrypt(cypher_text)
    return result


def sym_encrypt(data: str) -> monad.EitherMonad[str]:
    result = domain.sym_encrypt(data)
    return result


def sym_decrypt(cypher_text: str) -> monad.EitherMonad[str]:
    result = domain.sym_decrypt(cypher_text)
    return result

def generate_random_secret_url_safe():
    return domain.generate_random_secret_url_safe()


def jwks_import_from_pems(pem_jwks: list[tuple[str, str]]):
    return domain.public_key.jwks_import_from_pems(pem_jwks)


def create_jwks_from_jwks(jwk_results: list[monad.EitherMonad[jwk.JWK]]):
    return domain.create_jwks_from_jwks(jwk_results)


def get_jwks():
    return domain.get_jwks()


# Helpers


def token_config():
    return config.Configuration().token_for_env_as_dict(env.Env.env).value
