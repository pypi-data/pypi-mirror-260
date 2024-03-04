from __future__ import annotations
from typing import Protocol, Tuple, Optional

from pymonad.maybe import Maybe

from eoslib import domain

KeyFromCache = bool
KEKKid = str
Kid = str
CypherText = str
EncryptedKey = Tuple[KEKKid, CypherText]  # Type Returned from a KEK encrypt function
ExportableKeyTuple = Tuple[KEKKid, Kid, CypherText]  # Type returned from a exporting key fn
AddableExportableKeyTuple = Tuple[KeyFromCache, Optional[KEKKid], Maybe[CypherText]]  # Type returned from a exportingkey generation fn


class KeyCacherProtocol(Protocol):

    def read(self) -> Tuple[bool, str]:
        ...

    def write(self, **args) -> domain.Key:
        ...

    def write_without_env_mutation(self, **args) -> domain.Key:
        ...

    def key_use(self) -> domain.KeyUse:
        ...
