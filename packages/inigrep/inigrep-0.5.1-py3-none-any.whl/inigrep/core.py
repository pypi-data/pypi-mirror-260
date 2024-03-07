#!/usr/bin/python3

from __future__ import annotations

import functools
import os
import re
import sys
import typing


class NIL:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


PrefixT = typing.NewType('PrefixT', str)

ClonedLineT = typing.NewType('ClonedLineT', str)
KeyT = typing.NewType('KeyT', str)
KeypathT = typing.NewType('KeypathT', str)
LineT = typing.NewType('LineT', str)
RawValueT = typing.NewType('RawValueT', str)
SectionT = typing.NewType('SectionT', str)
ValueT = typing.NewType('ValueT', str)

NoClonedLineT = NIL('NoClonedLineT')
NoKey = NIL('NoKey')
NoKeypath = NIL('NoKeypath')
NoRawValue = NIL('NoRawValue')
NoSection = NIL('NoSection')
NoValue = NIL('NoValue')

MaybeClonedLineT = typing.Union[ClonedLineT, NIL]
MaybeKeyT = typing.Union[KeyT, NIL]
MaybeKeypathT = typing.Union[KeypathT, NIL]
MaybeRawValueT = typing.Union[RawValueT, NIL]
MaybeSectionT = typing.Union[SectionT, NIL]
MaybeValueT = typing.Union[ValueT, NIL]

IniDataT = dict[KeypathT, typing.List[ValueT]]
IniRawDataT = dict[KeypathT, typing.List[RawValueT]]

ClonedLineGenT = typing.Iterator[ClonedLineT]
KeyGenT = typing.Iterator[KeyT]
KeypathGenT = typing.Iterator[KeypathT]
LineGenT = typing.Iterator[LineT]
RawValueGenT = typing.Iterator[RawValueT]
SectionGenT = typing.Iterator[SectionT]
ValueGenT = typing.Iterator[ValueT]


class KeypathError(ValueError):
    pass


def check_kpath(v, vn, t):
    if not isinstance(v, t):
        raise KeypathError("invalid type: %s must be %s, got %s"
                           % (vn, t.__name__, type(v).__name__))


class Unit:
    """
    A parsed line
    """

    @classmethod
    def mkcomment(cls,
                  ctx_section: MaybeSectionT,
                  raw_line: LineT,
                  ) -> Unit:
        return cls(ctx_section, raw_line)

    @classmethod
    def mksection(cls,
                  ctx_section: MaybeSectionT,
                  raw_line: LineT,
                  section: SectionT,
                  ) -> Unit:
        return cls(section, raw_line, section=section)

    @classmethod
    def mkjunk(cls,
               ctx_section: MaybeSectionT,
               raw_line: LineT,
               ) -> Unit:
        return cls(ctx_section, raw_line)

    def __init__(self,
                 ctx_section: MaybeSectionT,
                 raw_line: LineT,
                 section: MaybeSectionT = NoSection,
                 key: MaybeKeyT = NoKey,
                 value: MaybeValueT = NoValue,
                 raw_value: MaybeRawValueT = NoRawValue,
                 ):
        self.raw_line = raw_line
        self.ctx_section = ctx_section
        self.section = section
        self.key = key
        self.value = value
        self.raw_value = raw_value

    def __str__(self):
        cn = self.__class__.__name__
        return f'{cn}[{self.ctx_section}](s={self.section},k={self.key})'

    @property
    def keypath(self) -> MaybeKeypathT:
        if isinstance(self.ctx_section, NIL):
            return NoKeypath
        if isinstance(self.key, NIL):
            return NoKeypath
        return KeypathT(self.ctx_section + '.' + self.key)

    @property
    def cloned_lines(self) -> ClonedLineGenT:
        if not isinstance(self.section, NIL):
            yield ClonedLineT('')
            yield ClonedLineT(f'[{self.section}]')
        if isinstance(self.ctx_section, NIL):
            return
        if isinstance(self.key, NIL):
            return
        yield ClonedLineT(f'    {self.key} ={self.raw_value}')


UnitGenT = typing.Iterator[Unit]


class Cond:

    @classmethod
    def from_arg(cls, arg: str,
                 require_key: bool = True,
                 require_sct: bool = True) -> Cond:
        def refuse_kp(msg):
            raise KeypathError("invalid keypath: %r is %s" % (arg, msg))
        if not isinstance(arg, str):
            raise refuse_kp("%s, need str" % type(arg).__name__)
        if '.' not in arg:
            refuse_kp("missing period")
        sct, key = arg.rsplit('.', maxsplit=1)
        if require_key and require_sct and not key and not sct:
            refuse_kp("missing section and key")
        if require_key and not key:
            refuse_kp("missing key")
        if require_sct and not sct:
            refuse_kp("missing section")
        if not sct and not key:
            return AlwaysMatchingCond()
        if not sct and key:
            # this is always invalid no matter require_*
            refuse_kp("missing section")
        if sct and not key:
            return SectionCond._from_arg(sct)
        if sct and key:
            return KeypathCond(SectionCond._from_arg(sct),
                               KeyCond._from_arg(key))
        raise KeypathError("unknown error")

    @classmethod
    def from_sct(cls, sct: str) -> Cond:
        if not isinstance(sct, str):
            raise KeypathError("invalid type: section must be str, got %s"
                               % type(sct).__name__)
        if not sct:
            raise KeypathError(r"section must not be empty: %r" % sct)
        if r']' in sct:
            raise KeypathError(r"invalid char ']' in section name: %r" % sct)
        return SectionCond(sct)

    def __init__(self, pat: typing.Any):
        self.pat = pat

    def __str__(self):
        cn = self.__class__.__name__
        return f'{cn}(pat={self.pat})'

    def match(self, unit: Unit) -> bool:
        raise NotImplementedError


class AlwaysMatchingCond(Cond):

    def __init__(self):
        pass

    def __str__(self):
        cn = self.__class__.__name__
        return f'{cn}()'

    def match(self, unit: Unit) -> bool:
        return True


class SectionCond(Cond):

    @classmethod
    def _from_arg(cls, arg: str) -> SectionCond:
        if r']' in arg:
            raise KeypathError(r"invalid char ']' in section name: %r" % arg)
        return cls(arg)

    def __init__(self, want_sct: str):
        self.want_sct = want_sct

    def __str__(self):
        cn = self.__class__.__name__
        return f'{cn}(want={self.want_sct})'

    def match(self, unit: Unit) -> bool:
        return unit.ctx_section == self.want_sct


class KeyCond(Cond):

    @classmethod
    def _from_arg(cls, arg: str) -> KeyCond:
        if r'\\'[0] in arg:
            raise KeypathError(r"invalid char '\' in key name: %r" % arg)
        if r'[' in arg:
            raise KeypathError(r"invalid char '[' in key name: %r" % arg)
        if r'=' in arg:
            raise KeypathError(r"invalid char '=' in key name: %r" % arg)
        return cls(arg)

    def __init__(self, pat: str):
        self.pat = pat

    def __str__(self):
        cn = self.__class__.__name__
        return f'{cn}(want={self.pat})'

    def match(self, unit: Unit) -> bool:
        return unit.key == self.pat


class KeypathCond(Cond):

    def __init__(self, sctcond: SectionCond, keycond: KeyCond):
        self.sctcond = sctcond
        self.keycond = keycond

    def __str__(self):
        cn = self.__class__.__name__
        return f'{cn}(s={self.sctcond},k={self.keycond})'

    def match(self, unit: Unit) -> bool:
        return self.sctcond.match(unit) and self.keycond.match(unit)


def extract_sections(units: typing.Iterator[Unit]) -> SectionGenT:
    seen = set()
    for unit in units:
        if isinstance(unit.section, NIL):
            continue
        if unit.section in seen:
            continue
        seen.add(unit.section)
        yield unit.section


def extract_clones(units: typing.Iterator[Unit]) -> ClonedLineGenT:
    for unit in units:
        if isinstance(unit.cloned_lines, NIL):
            continue
        for cloned_line in unit.cloned_lines:
            yield cloned_line


def extract_keypaths(units: typing.Iterator[Unit]) -> KeypathGenT:
    seen = set()
    for unit in units:
        if isinstance(unit.keypath, NIL):
            continue
        if unit.keypath in seen:
            continue
        seen.add(unit.keypath)
        yield unit.keypath


def extract_keys(units: typing.Iterator[Unit]) -> KeyGenT:
    seen = set()
    for unit in units:
        if isinstance(unit.key, NIL):
            continue
        if unit.key in seen:
            continue
        seen.add(unit.key)
        yield unit.key


def extract_values(units: typing.Iterator[Unit]) -> ValueGenT:
    for unit in units:
        if isinstance(unit.value, NIL):
            continue
        yield unit.value


def extract_raw_values(units: typing.Iterator[Unit]) -> RawValueGenT:
    for unit in units:
        if isinstance(unit.raw_value, NIL):
            continue
        yield unit.raw_value


def mkpipe(reader: LineGenT,
           cond: Cond,
           extractor: typing.Callable[[typing.Iterator[Unit]], typing.Any],
           ):
    parser = Parser()
#   matched = []
#   units = list(parser.parse(reader))
#   for unit in units:
#       print('mkpipe():==========')
#       print(f'mkpipe():unit={unit}')
#       print(f'mkpipe():cond={cond}')
#       print('mkpipe():----------')
#       print(f'mkpipe():unit.raw_line={unit.raw_line!r}')
#       if not cond.match(unit):
#           print('mkpipe():...not matched')
#           continue
#       print('mkpipe():...YES matched')
#       matched.append(unit)
#   print(f'mkpipe():len(matched)={len(matched)}')
#   for thing in extractor(matched):
#       print(f'mkpipe():thing={thing}')
#       yield thing
#   return extractor(matched)
    units = (unit for unit in parser.parse(reader)
             if cond.match(unit))
    return extractor(units)


class Parser:
    """
    Parse lines to units
    """

    def __init__(self):
        self.ctx_section = NoSection

    def _parse_line(self,
                    line: LineT,
                    ctx_section: MaybeSectionT = NoSection
                    ) -> Unit:
        def strip_raw(V):
            return re.sub(r'  *[#;].*', '', V.strip())
        if re.match(r'^\s*[#;]', line):
            return Unit.mkcomment(ctx_section, line)
        if re.match(r'^\s*\[[^]]+\]', line):
            left, _ = line.split(']', maxsplit=1)
            _, sctn = left.split('[', maxsplit=1)
            return Unit.mksection(ctx_section, line, SectionT(sctn))
        if '=' not in line:
            return Unit.mkjunk(ctx_section, line)
        key, raw_value = line.lstrip().split('=', 1)
        return Unit(
            ctx_section, line,
            NoSection,
            KeyT(key.strip()),
            ValueT(strip_raw(raw_value)),
            RawValueT(raw_value),
        )

    def parse(self,
              lines: LineGenT,
              ) -> UnitGenT:
        for line in lines:
            unit = self._parse_line(line, self.ctx_section)
            self.ctx_section = unit.ctx_section
            yield unit


def _r_clone(reader: LineGenT, kpath: str = '.') -> ClonedLineGenT:
    """
    Return replica of INI file provided by *reader*.
    """
    pipe = mkpipe(
        reader=reader,
        cond=Cond.from_arg(kpath, require_sct=False, require_key=False),
        extractor=extract_clones,
    )
    for line in pipe:
        yield ClonedLineT(line)


def _r_values(reader: LineGenT, kpath: str) -> ValueGenT:
    """
    Return list of values found by *reader* at key path *kpath*.

    *kpath* must be key path, i.e. string containing section and
    key names delimited by period.

    *reader* must be instance of FileReader generator or any similar
    generator that will yield lines.
    """
    pipe = mkpipe(
        reader=reader,
        cond=Cond.from_arg(kpath),
        extractor=extract_values,
    )
    for line in pipe:
        yield ValueT(line)


def _r_raw_values(reader: LineGenT, kpath: str) -> RawValueGenT:
    """
    Return list of raw values found by *reader* at key path *kpath*.

    Same as _r_values(), but uses raw inigrep engine, which keeps in-line
    comments and value leading/trailing whitespace.
    """
    pipe = mkpipe(
        reader=reader,
        cond=Cond.from_arg(kpath),
        extractor=extract_raw_values,
    )
    for line in pipe:
        yield RawValueT(line)


def _r_list_sections(reader: LineGenT) -> SectionGenT:
    """
    Return list of sections found by *reader*.
    """
    pipe = mkpipe(
        reader=reader,
        cond=AlwaysMatchingCond(),
        extractor=extract_sections,
    )
    for line in pipe:
        yield SectionT(line)


def _r_list_keys(reader: LineGenT, section: str) -> KeyGenT:
    """
    Return list of keys found by *reader* under *section*.
    """
    pipe = mkpipe(
        reader=reader,
        cond=Cond.from_sct(section),
        extractor=extract_keys,
    )
    for line in pipe:
        yield KeyT(line)


def _r_list_paths(reader: LineGenT, keypath: str = '.') -> KeypathGenT:
    """
    Return list of all key paths found by *reader*.
    """
    pipe = mkpipe(
        reader=reader,
        cond=Cond.from_arg(keypath, require_sct=False, require_key=False),
        extractor=extract_keypaths,
    )
    for line in pipe:
        yield KeypathT(line)


def FileReader(files: list[str]) -> LineGenT:
    """
    Line generator that reads multiple files
    """
    for path in files:
        for line in SingleFileReader(path):
            yield line


def ExistingFileReader(files: list[str]) -> LineGenT:
    """
    Line generator that reads multiple existent files

    Non-existent files are silently ignored.
    """
    for path in files:
        if not os.path.exists(path):
            continue
        for line in SingleFileReader(path):
            yield line


def SingleFileReader(path: str) -> LineGenT:
    """
    Line generator that reads single path
    """
    if path == '-':
        while True:
            line = sys.stdin.readline()
            if line:
                yield LineT(line[:-1])
            else:
                return
    else:
        with open(path, 'r') as fp:
            while True:
                line = fp.readline()
                if line:
                    yield LineT(line[:-1])
                else:
                    return
