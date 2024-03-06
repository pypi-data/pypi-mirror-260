""" This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

Created on Aug 10, 2021

@author: pymancer@gmail.com (polyanalitika.ru)
"""
from __future__ import annotations

from abc import ABCMeta
from typing import Optional, Union, List, Dict, Any
from jsqlib.helpers.constants import POSTGRESQL_DIALECT
from jsqlib.helpers.common import Tokenizer
from jsqlib.helpers.types import BL_T, SCBN_T, SCBND_T, SCBNLD_T


class Builder(metaclass=ABCMeta):
    """Base JSON to SQL expressions builder."""

    def __init__(
        self, constants: Optional[Dict[str, SCBN_T]] = None, tokenizer: Optional[Tokenizer] = None, **kwargs
    ) -> None:
        self._tokenizer = tokenizer or Tokenizer()
        self._tokenizer.constants = constants

    def build(self, query: Union[Dict[str, Any], List[dict]], dense: bool = True) -> str:
        chunks = list()
        query = query or dict()

        if isinstance(query, list):
            raise NotImplementedError

        for k, v in query.items():
            method = f"_{k.replace(' ', '_')}"
            if hasattr(self, method):
                chunks.append(getattr(self, method)(v))
            else:
                # generic function handler
                chunks.append(self._apply_(k, v))

        joined = ' '.join(chunks)

        return self._tokenizer.densify(joined) if dense else joined

    def _quote_(self, value):
        return self._tokenizer.dquote(value) if value else value

    def _stringify_(self, value: SCBN_T) -> str:
        return self._tokenizer.stringify(value)

    def _eval_(self, value: SCBND_T) -> str:
        if isinstance(value, dict):
            evaluated = self.build(value, dense=False)
        else:
            evaluated = self._stringify_(value)

        return evaluated

    def _apply_(self, name: str, args: List[SCBND_T]) -> str:
        merged = ','.join((self._eval_(arg) for arg in args))

        return f'{name}({merged})'

    def _alias_(self, alias: SCBND_T) -> str:
        return f'as {self._quote_(alias)}' if alias else ''

    def _enclose_(self, value: SCBNLD_T) -> str:
        if isinstance(value, list):
            enclosed = f"({','.join(self._eval_(v) for v in value)})"
        else:
            enclosed = f"({self._eval_(value)})"

        return enclosed

    def _commute_(self, value: List[SCBND_T], op: str) -> str:
        return f' {op} '.join((self._eval_(v) for v in value))

    def _combine_(self, value: Dict[str, SCBNLD_T], type_: str) -> str:
        return f'{type_} {self.build(value, dense=False)}'

    def _calc_(self, value: List[SCBND_T], op: str) -> str:
        return f'({self._commute_(value, op=op)})'

    def _columns_(self, columns: List[str]) -> str:
        chunks = [self._quote_(c) for c in columns]

        return f"({','.join(chunks)})"

    def _values_(self, values: List[list]) -> str:
        chunks = list()
        for row in values:
            chunks.append(f"( {','.join((self._stringify_(c) for c in row))})")

        return ','.join(chunks)

    def _from_(self, value: Dict[str, Any], type_: str = '') -> str:
        items = list()

        if type_:
            items.append(type_)

        if lateral := value.pop('lateral', None):
            alias = self._alias_(lateral.pop('alias', '')) if lateral else ''
            items.append(f'lateral {self._eval_(lateral)} {alias}')

        if enclose := value.pop('enclose', None):
            items.append(self._enclose_(enclose))

        if values := value.pop('values', None):
            items.append(f'(values {self._values_(values)})')

        if name := value.pop('name', None):
            items.append(self._quote_(name))

        if columns := value.pop('columns', None):
            items.append(self._columns_(columns))

        if using := value.pop('using', ''):
            items.append(f"using ({','.join(self._quote_(c) for c in using)})")

        if alias := value.pop('alias', ''):
            items.append(self._alias_(alias))

        if on := value.pop('on', ''):
            items.append(f"on {self._eval_(on)}")

        if value:
            items.append(self._eval_(value))

        return ' '.join(items)

    def _enclose(self, value: SCBNLD_T) -> str:
        return self._enclose_(value)

    def _value(self, value: SCBN_T) -> str:
        return self._stringify_(value)

    def _optional(self, value: Dict[str, SCBND_T]) -> str:
        optional = list()

        for k, v in value.items():
            optional.append(f"{k} => {self._eval_(v)}")

        return ','.join(optional)

    def _select(self, value: List[dict], distinct: bool = False) -> str:
        select = 'select distinct' if distinct else 'select'
        columns = list()
        ons = list()

        for column in value:
            if distinct and column.get('on', False):
                ons.append(self._eval_(column['eval']))
            else:
                evaluated = ''

                if 'eval' in column:
                    evaluated = self._eval_(column['eval'])
                elif 'name' in column:
                    evaluated = self._quote_(column['name'])

                if evaluated:
                    if 'alias' in column:
                        evaluated += f" {self._alias_(column['alias'])}"

                    columns.append(evaluated)

        if ons:
            select += ' on'
            ons = f"({','.join(ons)})"
        else:
            ons = ''

        if columns:
            columns = f" {','.join(columns)}"
        else:
            columns = ' *'

        return f'{select}{ons}{columns}'

    def _select_distinct(self, value: List[dict]) -> str:
        return self._select(value, distinct=True)

    def _with(self, value: Dict[str, Any], recursive: bool = False) -> str:
        with_ = 'with recursive' if recursive else 'with'

        chunks = list()
        for k, v in value.items():
            if columns := v.pop('columns', ''):
                columns = self._columns_(columns)

            chunks.append(f"{self._quote_(k)}{columns} as ({self.build(v, dense=False)})")

        return f"{with_} {', '.join(chunks)}"

    def _with_recursive(self, value: Dict[str, SCBND_T]) -> str:
        return self._with(value, recursive=True)

    def _union(self, value: Dict[str, SCBNLD_T], type_: str = '') -> str:
        union = f'union {type_}' if type_ else 'union'
        return self._combine_(value, union)

    def _union_all(self, value: Dict[str, SCBNLD_T]) -> str:
        return self._union(value, type_='all')

    def _union_distinct(self, value: Dict[str, SCBNLD_T]) -> str:
        return self._union(value, type_='distinct')

    def _intersect(self, value: Dict[str, SCBNLD_T], type_: str = '') -> str:
        intersect = f'intersect {type_}' if type_ else 'intersect'
        return self._combine_(value, intersect)

    def _intersect_all(self, value: Dict[str, SCBNLD_T]) -> str:
        return self._intersect(value, type_='all')

    def _intersect_distinct(self, value: Dict[str, SCBNLD_T]) -> str:
        return self._intersect(value, type_='distinct')

    def _except(self, value: Dict[str, SCBNLD_T], type_: str = '') -> str:
        except_ = f'except {type_}' if type_ else 'except'
        return self._combine_(value, except_)

    def _except_all(self, value: Dict[str, SCBNLD_T]) -> str:
        return self._except(value, type_='all')

    def _except_distinct(self, value: Dict[str, SCBNLD_T]) -> str:
        return self._except(value, type_='distinct')

    def _from(self, value: List[dict]) -> str:
        return f"from {','.join((self._from_(v) for v in value))}"

    def _join(self, value: Dict[str, SCBND_T], type_: str = '') -> str:
        return self._from_(value, type_=f'{type_} join')

    def _inner_join(self, value: Dict[str, SCBND_T]) -> str:
        return self._join(value, type_='inner')

    def _left_join(self, value: Dict[str, SCBND_T]) -> str:
        return self._join(value, type_='left')

    def _right_join(self, value: Dict[str, SCBND_T]) -> str:
        return self._join(value, type_='right')

    def _full_join(self, value: Dict[str, SCBND_T]) -> str:
        return self._join(value, type_='full')

    def _cross_join(self, value: Dict[str, SCBND_T]) -> str:
        return self._join(value, type_='cross')

    def _where(self, value: Dict[str, BL_T]) -> str:
        return f'where {self._eval_(value)}'

    def _group_by(self, value: List[SCBND_T]) -> str:
        return f"group by {','.join(self._eval_(v) for v in value)}"

    def _having(self, value: Dict[str, SCBNLD_T]) -> str:
        return f'having {self._eval_(value)}'

    def _order_by(self, value: List[SCBND_T]) -> str:
        columns = list()

        for v in value:
            if isinstance(v, dict):
                chunks = [self._eval_(v.pop('value', None))]

                if v.pop('desc', False):
                    chunks.append('desc')

                if 'using' in v:
                    using = self._eval_(v.pop('using'))
                    chunks.append(f'using {using}')

                columns.append(' '.join(chunks))
            else:
                columns.append(self._eval_(v))

        return f"order by {','.join(columns)}" if columns else ''

    def _limit(self, value: Dict[str, SCBND_T]) -> str:
        return f'limit {self._eval_(value)}'

    def _offset(self, value: Dict[str, SCBND_T]) -> str:
        return f'offset {self._eval_(value)}'

    def _is_distinct_from(self, value: List[str], negate: bool = False) -> str:
        op = 'is not distinct from' if negate else 'is distinct from'
        return f'{self._stringify_(value[0])} {op} {self._stringify_(value[-1])}'

    def _is_not_distinct_from(self, value: List[str]) -> str:
        return self._is_distinct_from(value, negate=True)

    def _eq(self, value: List[SCBND_T]) -> str:
        return self._commute_(value, op='=')

    def _neq(self, value: List[SCBND_T]) -> str:
        return self._commute_(value, op='!=')

    def _lt(self, value: List[SCBND_T]) -> str:
        return self._commute_(value, op='<')

    def _gt(self, value: List[SCBND_T]) -> str:
        return self._commute_(value, op='>')

    def _lte(self, value: List[SCBND_T]) -> str:
        return self._commute_(value, op='<=')

    def _gte(self, value: List[SCBND_T]) -> str:
        return self._commute_(value, op='>=')

    def _is(self, value: List[SCBND_T], negate: bool = False) -> str:
        condition = 'is not' if negate else 'is'
        return f'{self._eval_(value[0])} {condition} {self._eval_(value[-1])}'

    def _is_not(self, value: List[SCBND_T]) -> str:
        return self._is(value, negate=True)

    def _add(self, value: List[SCBND_T]) -> str:
        return self._calc_(value, op='+')

    def _sub(self, value: List[SCBND_T]) -> str:
        return self._calc_(value, op='-')

    def _mult(self, value: List[SCBND_T]) -> str:
        return self._calc_(value, op='*')

    def _div(self, value: List[SCBND_T]) -> str:
        return self._calc_(value, op='/')

    def _pow(self, value: List[SCBND_T]) -> str:
        return self._calc_(value, op='^')

    def _mod(self, value: List[SCBND_T]) -> str:
        return self._calc_(value, op='%')

    def _and(self, value: List[SCBND_T]) -> str:
        return self._calc_(value, op='and')

    def _or(self, value: List[SCBND_T]) -> str:
        return self._calc_(value, op='or')

    def _in(self, value: List[SCBND_T], negate: bool = False) -> str:
        op = 'not in' if negate else 'in'
        check = ','.join((self._eval_(v) for v in value[1:]))
        return f"{self._eval_(value[0])} {op} ({check})"

    def _not_in(self, value: List[SCBND_T]) -> str:
        return self._in(value, negate=True)

    def _cast(self, value: List[SCBND_T]) -> str:
        return f'cast ({self._eval_(value[0])} as {self._eval_(value[-1])})'

    def _like(self, value: List[SCBND_T], negate: bool = False) -> str:
        condition = 'not like' if negate else 'like'
        return f'{self._eval_(value[0])} {condition} {self._eval_(value[-1])}'

    def _not_like(self, value: List[SCBND_T]) -> str:
        return self._like(value, negate=True)

    def _exists(self, value: Dict[str, SCBNLD_T], negate: bool = False) -> str:
        condition = 'not exists' if negate else 'exists'
        return f'{condition} ({self.build(value, dense=False)})'

    def _not_exists(self, value: Dict[str, SCBNLD_T]) -> str:
        return self._exists(value, negate=True)

    def _between(self, value: List[SCBND_T], negate: bool = False) -> str:
        condition = 'not between' if negate else 'between'
        check = self._eval_(value[0])
        left = self._eval_(value[1])
        right = self._eval_(value[-1])

        return f'{check} {condition} {left} and {right}'

    def _not_between(self, value: List[SCBND_T]) -> str:
        return self._between(value, negate=True)

    def _case(self, value: Dict[str, Any]) -> str:
        alias = self._alias_(value.get('alias', ''))
        else_ = self._eval_(value.get('else', ''))
        else_ = f'else {else_}' if else_ else else_
        expression = self._eval_(value.get('expression', ''))
        case = f'case {expression}' if expression else 'case'

        conditions = list()
        for k in value.get('conditions', list()):
            when = f"when {self._eval_(k.get('when', ''))}"
            then = f"then {self._eval_(k.get('then', ''))}"
            conditions.append(' '.join((when, then)))

        return ' '.join([case, ' '.join(conditions), else_, 'end', alias])

    def _over(self, value: Dict[str, Any]) -> str:
        if partition := value.get('partition by', ''):
            partition = f"partition by {','.join((self._eval_(v) for v in partition))}"

        order = self._order_by(value.get('order by', ''))

        return f"over({partition} {order})"

    def _insert(self, value: Dict[str, Any]) -> str:
        name = self._quote_(value.pop('name'))

        if columns := value.pop('columns', ''):
            columns = f"({','.join((self._quote_(c) for c in columns))})"

        if values := value.pop('values', ''):
            values = f'values {self._values_(values)}'

        elif value:
            values = self._eval_(value)

        return f"insert into {name}{columns} {values}"

    def _update(self, value: Dict[str, Any]) -> str:
        data = ''
        alias = value.pop('alias', '')

        if columns := value.get('set', ''):
            chunks = list()

            for c in columns:
                chunks.append(f"{self._quote_(c['name'])} = {self._eval_(c['eval'])}")

            data = f"set {','.join(chunks)}"

        return f"update {self._quote_(value.get('name', ''))} {alias} {data}"

    def _delete(self, value: Dict[str, Any]) -> str:
        if using := value.pop('using', ''):
            chunks = list()

            for entity in using:
                if isinstance(entity, dict):
                    if name := entity.pop('name', None):
                        name = self._quote_(name)

                    if columns := entity.pop('columns', None):
                        columns = self._columns_(columns)

                    if values := entity.pop('values', None):
                        values = f'(values {self._values_(values)})'

                    if name and columns and values:
                        chunks.append(' '.join((values, 'as', name, columns)))
                else:
                    chunks.append(self._quote_(entity))

            using = f"using {','.join(chunks)}" if chunks else ''

        return f"delete from {self._quote_(value['name'])} {using}"

    def _returning(self, value: List[SCBND_T]) -> str:
        returning = list()

        for v in value:
            returning.append(self._eval_(v))

        return f"returning {','.join(returning)}"

    def _on_conflict(self, value: Dict[str, Any]) -> str:
        if columns := value.pop('columns', ''):
            columns = self._columns_(columns)

        if constraint := value.pop('constraint', ''):
            constraint = f'on constraint {self._stringify_(constraint)}'

        if update := value.pop('update', dict()):
            operation = self._update(update)
        else:
            operation = 'nothing'

        return f"on conflict {columns}{constraint} do {operation}"


class PGBuilder(Builder):
    """PostgreSQL builder."""


def get_builder(dialect: Optional[str] = POSTGRESQL_DIALECT, **kwargs) -> Builder:
    builders = kwargs.get('builders', {POSTGRESQL_DIALECT: PGBuilder})

    return builders[dialect](**kwargs)
