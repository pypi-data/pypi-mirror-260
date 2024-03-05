from eoslib import domain

from eoslib.util import env, chronos


def claims_builder(sub: str,
                   aud: str,
                   expires_in_seconds: int,
                   azp: str,
                   tenant_id: str,
                   gty: str,
                   iss: str):
    epoche_now = int(chronos.time_now(tz=chronos.tz_utc(), apply=[chronos.epoch()]))
    return dict(iss=iss,
                sub=sub,
                aud=aud,
                iat=epoche_now,
                exp=epoche_now + expires_in_seconds,
                azp=azp,
                gty=gty,
                tenant_id=tenant_id)
