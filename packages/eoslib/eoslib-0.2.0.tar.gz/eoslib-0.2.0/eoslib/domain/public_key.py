from __future__ import annotations
from typing import Tuple

from metis_crypto import jwk, jwt
import json

from eoslib import domain
from eoslib.util import monad, error


@monad.Try(error_cls=error.JWKSError)
def create_rsa_key_pair(kid, use: domain.KeyUse = None):
    """
    Args:
        kid: a unique id for the key

    Returns:
        JWK pub/priv key pair with a KID
    """
    return jwk.JWK.generate(kty='RSA', size=2048, kid=kid, use=use.value if use else use)


@monad.Try(error_cls=error.JWKSError)
def from_pem(pem: str):
    return jwk.JWK.from_pem(pem.encode('utf-8'))


def jwks_import_from_pems(pems: list[tuple[str, str]]) -> monad.Either[
    error.MonadicErrorAggregate, list[monad.Either[jwt.JWK]]]:
    """
    Takes a list of kid,pem tuples and converts them into jwks
    :param pems:
    :return:
    """
    results = [jwk_import_from_pem(pem, kid) for kid, pem in pems]
    if all(map(monad.maybe_value_ok, results)):
        return monad.Right(results)
    return monad.Left(error.MonadicErrorAggregate(results))


@monad.Try(error_cls=error.JWKSError)
def jwk_import_from_pem(pem: str, kid: str | None = None):
    """
    Takes a PEM formatted key, pub or private, and an optional KID and imports it into
    a JWK format
    :param pem:
    :param kid:
    :return:
    """
    key = jwt.JWK()
    key.import_from_pem(pem.encode('utf-8'), kid=kid)
    return key


@monad.Try(error_cls=error.JWKSError)
def export_pair_as_json(pair: jwk.JWK) -> monad.EitherMonad[str]:
    return pair.export()


@monad.Try(error_cls=error.JWKSError)
def load_pair_from_json(json_pair: str) -> monad.EitherMonad[jwk.JWK]:
    return jwk.JWK(**json.loads(json_pair))
