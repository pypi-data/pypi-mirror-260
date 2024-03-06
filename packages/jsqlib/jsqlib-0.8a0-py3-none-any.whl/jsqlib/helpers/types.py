""" This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

Created on Aug 14, 2021

@author: pymancer@gmail.com (polyanalitika.ru)
"""
from typing import Union
from typing_extensions import TypeAlias

C_T: TypeAlias = Union[int, float]
BL_T: TypeAlias = Union[bool, list]
LD_T: TypeAlias = Union[dict, list]
SD_T: TypeAlias = Union[str, dict]
SC_T: TypeAlias = Union[str, C_T]
SLD_T: TypeAlias = Union[str, LD_T]
CBN_T: TypeAlias = Union[C_T, bool, None]
SCB_T: TypeAlias = Union[SC_T, bool]
SCD_T: TypeAlias = Union[SC_T, dict]
SDB_T: TypeAlias = Union[SD_T, bool]
SCBD_T: TypeAlias = Union[SCB_T, dict]
SCBN_T: TypeAlias = Union[SCB_T, None]
SCBNL_T: TypeAlias = Union[SCBN_T, list]
SCBND_T: TypeAlias = Union[SCBN_T, dict]
SCBNLD_T: TypeAlias = Union[SCBNL_T, dict]
