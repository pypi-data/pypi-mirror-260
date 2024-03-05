# https://github.com/pallets/click/pull/2686

from typing import Any, Sequence

import click.parser
from click.types import ParamType


class ForwardParamType(ParamType):
    name = "text"

    def convert(self, value, param, ctx) -> Any:
        return value

    def __repr__(self) -> str:
        return "FORWARD"


#: A dummy parameter type that just does nothing except stops parsing options
#: and arguments when this argument is getting parsed.
FORWARD = ForwardParamType()


def _stop_process_args_for_options(self, state) -> bool:
    largs: Sequence[str] = state.largs
    for args in self._args:
        if type(args.obj.type) is type(FORWARD) and args.nargs < 0:
            return True
        if not largs:
            break
        largs = largs[args.nargs :]
    return False


def _process_args_for_options(self, state) -> None:
    while state.rargs:
        arg = state.rargs.pop(0)
        arglen = len(arg)
        # Double dashes always handled explicitly regardless of what
        # prefixes are valid.
        if arg == "--":
            return
        elif arg[:1] in self._opt_prefixes and arglen > 1:
            self._process_opts(arg, state)
        elif _stop_process_args_for_options(self, state):
            state.rargs.insert(0, arg)
            return
        elif self.allow_interspersed_args:
            state.largs.append(arg)
        else:
            state.rargs.insert(0, arg)
            return


def init():
    click.parser.OptionParser._process_args_for_options = _process_args_for_options


init()
