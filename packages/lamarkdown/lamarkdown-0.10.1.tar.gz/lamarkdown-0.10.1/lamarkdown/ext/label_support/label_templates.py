from __future__ import annotations
from . import counter_types
from . import standard_counter_types
from dataclasses import dataclass
import sys

if sys.version_info < (3, 11):
    # The 're' module doesn't support possessive quantifiers ('*+', etc.) until Python 3.11.
    import regex as re
else:
    import re


@dataclass
class LabelTemplate:
    prefix: str
    separator: str
    suffix: str
    parent_type: str | None
    counter_type: counter_types.CounterType | None
    inner_template: 'LabelTemplate' | None

    def __repr__(self):
        css_id = self.counter_type.css_id if self.counter_type else ''
        inner_spec = (
            ',*'    if self.inner_template is self
            else '' if self.inner_template is None
            else repr(self.inner_template)
        )
        if self.parent_type is None:
            return (f'{self.prefix}{css_id}{self.suffix}{inner_spec}')

        parent_spec = {'': 'X', 'ol': 'L'}.get(self.parent_type, self.parent_type)
        return (f'{self.prefix}{parent_spec}{self.separator}{css_id}{self.suffix}{inner_spec}')


class LabelTemplateException(Exception):
    pass


QUOTED_LITERAL = r'''
    ' ( [^'] | '' )*+ '
    |
    " ( [^"] | "" )*+ "
'''

LITERAL = fr'''
    (
        [^a-zA-Z0-9,'"] | {QUOTED_LITERAL}
    )++
'''

# Notes:
# * In <format>, '-' is allowed as an internal character only; any leading/trailing '-' will be
#   part of the prefix, separator or suffix.
TEMPLATE_REGEX = re.compile(fr'''(?x)
    \s*
    (?P<prefix> {LITERAL} )?
    (
        (
            (?P<parent> [XxLl] | [Hh][1-6]? )
            (?P<separator> {LITERAL} )
        )?+
        (?P<format> [a-zA-Z0-9] ([a-zA-Z0-9-]* [a-zA-Z0-9])? )
        (?P<suffix> {LITERAL} )?
    )?
    \s*
''')

QUOTED_LITERAL_REGEX = re.compile(f'(?sx){QUOTED_LITERAL}')
ESCAPED_QUOTES = {'"': re.compile('""'),
                  "'": re.compile("''")}


def parse_element_type(spec: str) -> str:
    spec = spec.lower()
    return {'x': '', 'l': 'ol'}.get(spec, spec)


def _repl_literal(match) -> str:
    quote = match.group()[0]
    text  = match.group()[1:-1]
    return ESCAPED_QUOTES[quote].sub(quote, text)


class LabelTemplateParser:

    DEFAULT = LabelTemplate(prefix = '', separator = '', suffix = '.', parent_type = '',
                            counter_type = standard_counter_types.get_counter_type('decimal'),
                            inner_template = None)

    def __init__(self):
        self._cache = {}

    def parse(self, template_str: str, error_msg_offset: int = 0) -> LabelTemplate:
        if template_str is None:
            raise ValueError

        template = self._cache.get(template_str)
        if template is not None:
            return template

        match = TEMPLATE_REGEX.match(template_str)
        if match is None:
            raise LabelTemplateException(f'Parse error in label template "{template_str}"')

        parent_type = None
        if (parent_spec := match.group('parent')) is not None:
            parent_type = parse_element_type(parent_spec)

        counter_type = None
        if (counter_name := match.group('format')) is not None:
            counter_type = standard_counter_types.get_counter_type(counter_name)
            if counter_type is None:
                raise LabelTemplateException(
                    f'Invalid counter type "{counter_name}" in label template "{template_str}"')

        template = LabelTemplate(
            prefix       = QUOTED_LITERAL_REGEX.sub(_repl_literal, match.group('prefix') or ''),
            separator    = QUOTED_LITERAL_REGEX.sub(_repl_literal, match.group('separator') or ''),
            suffix       = QUOTED_LITERAL_REGEX.sub(_repl_literal, match.group('suffix') or ''),
            parent_type  = parent_type,
            counter_type = counter_type,
            inner_template = None
        )

        match_end = match.end()
        error_msg_offset += match_end

        if match_end < len(template_str):
            if template_str[match_end] != ',':
                raise LabelTemplateException(
                    f'Parse error at index {error_msg_offset} in label template "{template_str}"')

            inner_template_str = template_str[match_end + 1:]
            template.inner_template = (
                template if inner_template_str.strip() == '*'
                else self.parse(inner_template_str, error_msg_offset)
            )

        self._cache[template_str] = template
        return template
