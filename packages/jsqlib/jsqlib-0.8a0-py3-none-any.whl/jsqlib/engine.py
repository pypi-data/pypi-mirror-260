""" This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

Created on Jul 29, 2021

@author: pymancer@gmail.com (polyanalitika.ru)
"""
import json
import sqlfluff

from copy import deepcopy
from typing import Optional, List, Dict, Type, Any
from jsonschema.validators import validator_for
from sqlfluff.core.dialects import dialect_selector
from jinja2 import Template
from jsqlib.core import Builder, get_builder
from jsqlib.helpers.constants import POSTGRESQL_DIALECT, QUERY_KEY
from jsqlib.helpers.types import LD_T, SLD_T, SDB_T, SCBN_T


class Query:
    """JSON to SQL query generator."""

    def __init__(
        self,
        raw: Optional[SLD_T] = None,
        constants: Optional[Dict[str, SCBN_T]] = None,
        bindings: Optional[Dict[str, SCBN_T]] = None,
        builder: Optional[Type[Builder]] = None,
        schema: Optional[SDB_T] = None,
        **kwargs,
    ) -> None:

        self._raw = deepcopy(raw) if isinstance(raw, dict) else raw
        self._bindings = bindings or dict()
        self._bound = None
        self._body = None
        self._sql = None

        self._validator = self._get_validator(schema)

        self.builder = builder or get_builder(constants=constants, **kwargs)

    @property
    def sql(self) -> str:
        if self._sql is None:
            self._sql = self._build()

        return self._sql

    @property
    def bound(self) -> LD_T:
        if self._bound is None:

            if isinstance(self._raw, str):
                raw = self._raw
            else:
                raw = json.dumps(self._raw or dict())

            self._bound = json.loads(Template(raw).render(self._bindings))

        return self._bound

    @property
    def body(self) -> LD_T:
        if self._body is None:
            self._body = self.bound.get(QUERY_KEY, self.bound) if isinstance(self.bound, dict) else self.bound

        return self._body

    @property
    def schema(self) -> dict:
        return self._validator.schema

    def validate(self) -> None:
        """Validates json query against schema."""
        self._validator.validate(self.bound)

    def _get_validator(self, schema: Optional[SDB_T] = None) -> Any:
        """Compiles valid schemas, ignores invalid ones."""
        if isinstance(schema, str):
            try:
                schema = json.loads(schema)
            except json.JSONDecodeError:
                pass

        if not isinstance(schema, dict):
            schema = True

        return validator_for(schema)(schema)

    def prettify(
        self, sql: Optional[str] = None, dialect: Optional[str] = None, rules: Optional[List[str]] = None
    ) -> str:

        sql = sql or self.sql
        dialect = dialect or POSTGRESQL_DIALECT

        if dialect == POSTGRESQL_DIALECT:
            dialect = 'postgres'

        try:
            dialect_selector(dialect)
        except KeyError:
            dialect = 'ansi'

        return sqlfluff.fix(sql, dialect=dialect, rules=rules) if sql else sql

    def _build(self, *args, **kwargs) -> str:
        built = ''

        if self.body is not None:
            self.validate()
            built = self.builder.build(self.body)

        return built
