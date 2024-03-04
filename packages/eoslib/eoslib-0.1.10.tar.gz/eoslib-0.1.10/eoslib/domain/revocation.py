from __future__ import annotations
from typing import Callable

from eoslib import domain
from eoslib.util import fn, monad


def revoke_previous_key(existing_key_result: monad.EitherMonad[domain.Key],
                        gracefully: bool = True,
                        after_revoke_fn: Callable = fn.identity):

    transition = 'rotate' if not gracefully else "graceful_rotate"

    new_state_result = domain.key_state_transition(from_state=existing_key_result.value.state,
                                                   with_transition=transition)

    if new_state_result.is_left():
        return new_state_result

    domain.KEYSTORE.change_key_state(kid=existing_key_result.value.kid,
                                     new_state=new_state_result.value)

    existing_key_result.map(after_revoke_fn)
    pass
