from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass
class ColumnSpec:
    name: str
    notnull: bool
    unique: bool
    dtype: str


@dataclass
class VectorScanResult:
    vec: np.ndarray
    extra: list[Any]

    def __str__(self):
        return f"VectorScanResult({','.join([str(item) for item in self.extra])})"

    def __repr__(self):
        return self.__str__()
