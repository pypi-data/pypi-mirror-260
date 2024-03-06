""" This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

Created on Aug 10, 2021

@author: pymancer@gmail.com (polyanalitika.ru)
"""
from __future__ import annotations

from re import sub as resub
from typing import Optional, Set, Dict
from dataclasses import dataclass, field
from functools import total_ordering
from box import Box
from jsqlib.helpers.constants import WRAP, TRANSLATORS, POSTGRESQL_DIALECT, NoneType
from jsqlib.helpers.types import CBN_T, SCBN_T


class Tokenizer:
    def __init__(
        self,
        constants: Optional[Dict[str, SCBN_T]] = None,
        wrap: Optional[Box] = None,
        translator: Optional[Box] = None,
    ) -> None:

        self.constants = constants or dict()
        self.wrap = wrap or WRAP
        self.translator = translator or TRANSLATORS[POSTGRESQL_DIALECT]

    @staticmethod
    def densify(value: str) -> str:
        """Removes duplicate spaces."""
        return resub(' +', ' ', value)

    @staticmethod
    def get_token_tree(tokens: Set[Token]) -> Token:
        """Builds tree from tokens and returns root token as tree."""
        ordered = sorted(tokens)
        adopted = set()

        for idx, child in enumerate(ordered, start=1):
            for parent in ordered[idx:]:
                if child not in adopted and child in parent:
                    parent.children.add(child)
                    adopted.add(child)

        return ordered[-1]  # last element will be the whole tokenized value

    def _quote(self, value: str, double=False) -> str:
        type_ = 'double' if double else 'single'
        merged = value
        left = self.translator.quote[type_].left
        right = self.translator.quote[type_].right
        delimiter = self.translator.quote[type_].delimiter

        if delimiter:
            merged = f'{left}{delimiter}{right}'.join(value.split(delimiter))

        return f'{left}{merged}{right}'

    def dquote(self, value: str) -> str:
        """Double quotes a string, handles delimiters."""
        return self._quote(value, double=True)

    def const(self, key: str, wrapped: str) -> str:
        """Substitutes value with corresponding constant if any."""
        if key in self.constants:
            result = str(self.cast(self.constants[key]))
        else:
            result = wrapped

        return result

    def squote(self, value: str) -> str:
        """Single quotes a string."""
        return self._quote(value, double=False)

    def unquote(self, wrapped: str) -> str:
        """Removes surrounding single or double quotes."""
        wrap_len = self.wrap.quote_len + self.wrap.key_len
        return wrapped[wrap_len:-wrap_len]

    def requote(self, value: str, token: Token) -> str:
        """Quotes, unquotes, cuts or even replaces the value according to the token indices."""
        result = value

        if token.operation:
            wrapper = value[: self.wrap.key_len] + value[-self.wrap.key_len :]
            inner = value[self.wrap.key_len : -self.wrap.key_len]
            wrap_len = self.wrap.quote_len + self.wrap.key_len

            if (
                token.operation == self.wrap.double.operation
                and wrapper == self.wrap.double.left + self.wrap.double.right
            ):

                result = self.dquote(inner)
            elif (
                token.operation == self.wrap.const.operation and wrapper == self.wrap.const.left + self.wrap.const.right
            ):

                result = self.const(inner, value)
            elif (
                token.operation == self.wrap.single.operation
                and wrapper == self.wrap.single.left + self.wrap.single.right
            ):

                result = self.squote(inner)
            elif (
                token.operation == self.wrap.unquote.operation
                and value[self.wrap.quote_len : wrap_len] == self.wrap.unquote.left
                and value[-wrap_len : -self.wrap.quote_len] == self.wrap.unquote.right
            ):

                result = self.unquote(value)
        elif token.escaped:
            # escaped wrapper
            escape_len = self.wrap.escape_len + self.wrap.escape_len
            if value[:escape_len] == self.wrap.left_escape + self.wrap.left_escape:
                result = value[self.wrap.escape_len :]
            elif value[-escape_len:] == self.wrap.right_escape + self.wrap.right_escape:
                result = value[: -self.wrap.escape_len]

        return result

    def tokenize(self, value: str) -> Token:
        """Generates a set of wrapped tokens from str value."""
        step = 1
        value_len = len(value)
        wrapped = set()  # chunks to merge
        # already handled wrapper indices
        burnt_left = set()

        ridx = self.wrap.key_len  # leaving space for the left operator
        while ridx < value_len:
            right = value[ridx : (right_origin := ridx + self.wrap.key_len)]

            if (
                (skipped_origin := ridx - self.wrap.key_len) not in burnt_left
                and ridx > self.wrap.key_len
                and value[(esc_idx := skipped_origin - step)] == self.wrap.left_escape
                and value[skipped_origin:ridx] in self.wrap.lefts
            ):
                # tokenizing skipped escaped left wrapper
                wrapped.add(Token(esc_idx, ridx, value=value[esc_idx:ridx], escaped=True, tokenizer=self))
                burnt_left.add(skipped_origin)

            if right in self.wrap.rights:
                operation = right[0]  # assuming that 1 character is enough to distinguish wrappers

                if value_len > right_origin and value[right_origin] == self.wrap.right_escape:
                    # tokenizing escaped right wrapper
                    esc_idx = right_origin + step
                    wrapped.add(Token(ridx, esc_idx, value=value[ridx:esc_idx], escaped=True, tokenizer=self))
                    ridx = esc_idx
                    continue

                pair = self.wrap.left_escape + operation
                lidx = ridx

                while lidx >= self.wrap.key_len:  # leaving space for the left operator
                    left = value[(left_origin := lidx - self.wrap.key_len) : lidx]

                    if left == pair:

                        if left_origin in burnt_left:
                            lidx -= self.wrap.key_len  # skipping burnt_left wrapper
                            continue

                        burnt_left.add(left_origin)

                        if left_origin > 0 and value[(esc_idx := left_origin - step)] == self.wrap.left_escape:
                            # tokenizing escaped left wrapper
                            wrapped.add(Token(esc_idx, lidx, value=value[esc_idx:lidx], escaped=True, tokenizer=self))
                            lidx = esc_idx
                            continue

                        if (
                            operation == self.wrap.unquote.operation
                            and value_len >= right_origin - left_origin + self.wrap.quote_len + self.wrap.quote_len
                        ):
                            # unquote token must include valid outer quotation marks
                            left_quote = value[left_origin - self.wrap.quote_len : left_origin]
                            right_quote = value[right_origin : right_origin + self.wrap.quote_len]

                            if (
                                left_quote == self.translator.quote.double.left
                                and right_quote == self.translator.quote.double.right
                            ) or (
                                left_quote == self.translator.quote.single.left
                                and right_quote == self.translator.quote.single.right
                            ):

                                left_origin -= self.wrap.quote_len
                                right_origin += self.wrap.quote_len

                        token = Token(
                            left_origin,
                            right_origin,
                            value=value[left_origin:right_origin],
                            operation=operation,
                            tokenizer=self,
                        )

                        for w in wrapped:
                            if token.intersect(w):
                                break  # tokens can't intersect
                        else:
                            wrapped.add(token)
                            ridx = right_origin
                            break

                    else:
                        lidx -= step  # moving to the next char
                else:
                    ridx += self.wrap.key_len  # pair not found, skipping orphan right wrapper
            else:
                ridx += step  # moving to the next char

        # root token
        root_wrap = value[: self.wrap.key_len]
        root_operation = root_wrap[-1] if root_wrap in self.wrap.lefts else ''
        wrapped.add(Token(0, value_len, value=value, operation=root_operation, tokenizer=self))

        return self.get_token_tree(wrapped)

    def cast(self, value: CBN_T) -> str:
        """Stringifies bools and nones."""
        result = value
        type_ = type(value)
        true = self.translator.cast.true
        false = self.translator.cast.false
        null = self.translator.cast.null

        if type_ == bool:
            result = true if value else false
        elif type_ == NoneType:
            result = null

        return result

    def stringify(self, value: SCBN_T) -> str:
        """Stringifies value by applying wrappers."""
        value_str = str(value)

        if isinstance(value, str):
            result = self.tokenize(value_str) if len(value) >= self.wrap.key_len + self.wrap.key_len else value
        else:
            result = self.cast(value)

        return str(result)


@total_ordering
@dataclass(frozen=True)
class Token:
    """Wrapped string or escaped wrapper."""

    lidx: int
    ridx: int
    value: str = field(default_factory=str)
    operation: str = field(default_factory=str)
    escaped: bool = False
    children: Set[Token] = field(default_factory=set)
    tokenizer: Optional[Tokenizer] = field(default_factory=Tokenizer)

    def __eq__(self, other: Token) -> bool:
        return self.lidx == other.lidx and self.ridx == other.ridx

    def __lt__(self, other: Token) -> bool:
        return self.ridx < other.ridx if self.ridx != other.ridx else self.lidx > other.lidx

    def __contains__(self, other: Token) -> bool:
        return other.lidx >= self.lidx and other.ridx <= self.ridx

    def __str__(self):
        merged = list()
        left_escaped = False
        right_escaped = False

        current = self
        for idx, c in enumerate(self.value):
            shifted = idx + self.lidx
            inherited = False

            for t in self.children:
                if t.lidx <= shifted < t.ridx:
                    inherited = True

                    if t != current:
                        merged.append(str(t))
                    current = t

                if t.escaped:
                    if t.lidx == self.lidx:
                        left_escaped = True
                    if t.ridx == self.ridx:
                        right_escaped = True

            if not inherited:
                merged.append(c)

        requoted = ''.join(merged)
        if not (left_escaped and right_escaped):
            # quote only if token has no escaped border tokens
            requoted = self.tokenizer.requote(requoted, self)

        return requoted

    def __hash__(self):
        return hash((self.lidx, self.ridx))

    def intersect(self, other):
        return (self.lidx <= other.lidx and other.lidx < self.ridx <= other.ridx) or (
            self.ridx > other.ridx and other.lidx <= self.lidx < other.ridx
        )
