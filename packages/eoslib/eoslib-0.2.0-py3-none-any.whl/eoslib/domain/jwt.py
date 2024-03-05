from __future__ import annotations

import json
from dataclasses import dataclass, field
from functools import partial

from metis_crypto.common import json_decode
from metis_crypto.jwe import JWE
from metis_crypto.jws import JWS
from metis_crypto.jwt import JWT
from metis_crypto.jwk import JWK
from pymonad.tools import curry
from eoslib.util import fn, monad, error, chronos

from eoslib import domain


class TokenError(error.BaseError):
    pass


@dataclass
class JwtPipline:
    signing_key: domain.CompiledKey
    claims: dict = field(default=None)
    jwt: JWT = field(default=None)
    token: str = field(default=None)


def generate_signed_jwt(claims: dict) -> monad.EitherMonad[str]:
    """
    Generates an RSA signed JWT is serialised form
    """
    result = (jwt_pipeline_builder(claims) >>
              generate_jwt >>
              sign >>
              serialise)

    if result.is_right():
        return monad.Right(result.value.token)
    return result


def decode_jwt_and_validate(encoded_jwt: str, no_sig: bool = False) -> dict:
    token = JWT(jwt=encoded_jwt)
    jwt = token.token

    if not isinstance(jwt, JWS):
        return monad.Left(error.JWTError("Token is not a JWT"))

    if 'kid' not in jwt.jose_header.keys():
        return monad.Left(error.JWTError("kid not found in JWT header."))

    if no_sig:
        return monad.Right(json.loads(token.token.objects['payload'].decode('UTF-8')))

    signing_key_result = domain.get_public_key_pair_by_kid(kid=jwt.jose_header['kid'])

    if not signing_key_result.is_right():
        return monad.Left(error.JWTError(f"Signing key with kid {jwt.jose_header['kid']} not found"))

    jwt.verify(signing_key_result.value)

    return monad.Right(json_decode(jwt.payload))


#
# Helper Functions
#

def jwt_pipeline_builder(claims: dict):
    maybe_sign_key = current_sig_key()

    if maybe_sign_key.is_right():
        return monad.Right(JwtPipline(signing_key=maybe_sign_key.value, claims=claims))
    return monad.Left(error.JWTError('Can not find a signing key'))


def current_sig_key() -> monad.EitherMonad[JWK]:
    return domain.build_key_by_use(domain.KeyUse.SIG)


def jse_decrypt():
    token = jtok.token
    if isinstance(token, JWE):
        token.decrypt(self.kkstore.server_keys[KEY_USAGE_ENC])
        # If an encrypted payload is received then there must be
        # a nested signed payload to verify the provenance.
        payload = token.payload.decode('utf-8')
        token = JWS()
        token.deserialize(payload)
    elif isinstance(token, JWS):
        pass
    else:
        raise TypeError("Invalid Token type: %s" % type(jtok))


def generate_jwt(jwt_value: JwtPipline) -> monad.EitherMonad[JwtPipline]:
    jwt_value.jwt = JWT({'kid': jwt_value.signing_key.compiled_key.kid,
                         'alg': 'RS256',
                         'kty':  jwt_value.signing_key.key.alg},
                        jwt_value.claims)
    return monad.Right(jwt_value)


def sign(jwt_value: JwtPipline) -> monad.EitherMonad[JwtPipline]:
    jwt_value.jwt.make_signed_token(jwt_value.signing_key.compiled_key)
    return monad.Right(jwt_value)


def serialise(jwt_value: JwtPipline) -> monad.EitherMonad[JwtPipline]:
    jwt_value.token = jwt_value.jwt.serialize()
    return monad.Right(jwt_value)


# def generate_expired_signed_jwt():
#     """
#     Generates an RSA signed JWT is serialised form which is expired
#     """
#     return jwt.encode(jwt_claims_expired(), rsa_private_key(), algorithm="RS256")


def generate_valid_signed_jwt():
    return generate_signed_jwt(rsa_private_key())


def is_jwt_claims_expired(claims):
    return claims['exp'] < int(chronos.time_now(tz=chronos.tz_utc(), apply=[chronos.epoch()]))
