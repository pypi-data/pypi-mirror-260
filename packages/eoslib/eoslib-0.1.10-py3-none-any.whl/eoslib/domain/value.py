from __future__ import annotations
from typing import Any
from enum import Enum
from dataclasses import dataclass
from eoslib import domain
class KeyUse(Enum):
    SIG = 'sig'
    ENC = 'enc'
    JWTENC = 'jwtenc'
    KEK = 'kek'
    JWKS = 'jwks'


@dataclass
class CompiledKey:
    key: domain.Key
    compiled_key: Any