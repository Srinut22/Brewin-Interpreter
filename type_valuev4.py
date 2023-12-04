import copy

from enum import Enum
from intbase import InterpreterBase
from env_v4 import EnvironmentManager

# Enumerated type for our different language data types


class Type(Enum):
    INT = 1
    BOOL = 2
    STRING = 3
    CLOSURE = 4
    NIL = 5
    OBJECT = 6


class Object:
    def __init__(self):
        self.prototype = None
        self.environment = {}
        self.type = Type.OBJECT

    def set_prototype(self, proto):
        self.prototype = proto

    def get(self, var_name):
        if var_name == "proto":
            return self.prototype
        if var_name in self.environment:
            return self.environment[var_name]
        elif self.prototype is not None:
            if self.prototype.type() != Type.NIL and self.prototype.value().environment is not self.environment:
                return self.prototype.value().get(var_name)
        return None

    def set(self, var_name, var_value, isCopied=False):
        if isCopied:
            self.environment[var_name] = copy.deepcopy(var_value)
        else:
            self.environment[var_name] = var_value


class Closure:
    def __init__(self, func_ast, env):
        self.captured_env = EnvironmentManager()
        temporary_env = env.get_env()
        for index in range(len(temporary_env)):
            for key in temporary_env[index].keys():
                if temporary_env[index][key].type() == Type.CLOSURE or temporary_env[index][key].type() == Type.OBJECT:
                    self.captured_env.set(key, temporary_env[index][key])
                else:
                    self.captured_env.set(
                        key, copy.deepcopy(temporary_env[index][key]))
        self.func_ast = func_ast
        self.type = Type.CLOSURE


# Represents a value, which has a type and its value
class Value:
    def __init__(self, t, v=None):
        self.t = t
        self.v = v

    def value(self):
        return self.v

    def type(self):
        return self.t

    def set(self, other):
        self.t = other.t
        self.v = other.v


def create_value(val):
    if val == InterpreterBase.TRUE_DEF:
        return Value(Type.BOOL, True)
    elif val == InterpreterBase.FALSE_DEF:
        return Value(Type.BOOL, False)
    elif isinstance(val, int):
        return Value(Type.INT, val)
    elif val == InterpreterBase.NIL_DEF:
        return Value(Type.NIL, None)
    elif isinstance(val, str):
        return Value(Type.STRING, val)


def get_printable(val):
    if val.type() == Type.INT:
        return str(val.value())
    if val.type() == Type.STRING:
        return val.value()
    if val.type() == Type.BOOL:
        if val.value() is True:
            return "true"
        return "false"
    return None
