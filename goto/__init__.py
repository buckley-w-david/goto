__version__ = "0.1.0"

from functools import wraps
from types import FunctionType
import dis
import io

_LOAD_GLOBAL = dis.opname.index("LOAD_GLOBAL")
_LOAD_DEREF = dis.opname.index("LOAD_DEREF")
_LOAD_METHOD = dis.opname.index("LOAD_METHOD")
_LOAD_CONST = dis.opname.index("LOAD_CONST")
_JUMP_ABSOLUTE = dis.opname.index("JUMP_ABSOLUTE")


class __GotoDocorator:
    def __init__(self, f):
        wraps(f)(self)
        code = dis.Bytecode(f)
        instr = [i for i in code]
        targets = {}
        gotos = {}
        for i1, i2, i3 in zip(instr, instr[1:], instr[2:]):
            if (
                (i1.opcode == _LOAD_GLOBAL or i1.opcode == _LOAD_DEREF)
                and i1.argval == f.__name__
                and i2.opcode == _LOAD_METHOD
                and i3.opcode == _LOAD_CONST
            ):
                if i2.argval == "label":
                    targets[i3.argval] = (
                        i3.offset + 6
                    ) // 2  # divide by 2 to get instruction offset from byte offset
                elif i2.argval == "goto":
                    gotos[i1.offset] = i3.argval

        writer = io.BytesIO()
        for i1 in instr:
            if i1.offset in gotos:
                target = targets[gotos[i1.offset]]
                writer.write(bytes([_JUMP_ABSOLUTE, target]))
            else:
                writer.write(bytes([i1.opcode, i1.arg or 0]))

        bytecode = writer.getvalue()
        code = code.codeobj.replace(co_code=bytecode)

        self.func = FunctionType(
            code, f.__globals__, f.__name__, f.__defaults__, f.__closure__
        )

    def goto(self, _: str):
        pass

    def label(self, _: str):
        pass

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


goto = __GotoDocorator
