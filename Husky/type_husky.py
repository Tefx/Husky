import wrap
import types
import class_husky

type_list = [
    types.NoneType,
    types.TypeType,
    types.BooleanType,
    types.IntType,
    types.LongType,
    types.FloatType,
    types.ComplexType,
    types.StringType,
    types.UnicodeType,
    types.TupleType,
    types.ListType,
    types.DictType,
    types.DictionaryType,
    types.FunctionType,
    types.LambdaType,
    types.GeneratorType,
    types.CodeType,
    types.ClassType,
    types.InstanceType,
    types.MethodType,
    types.UnboundMethodType,
    types.BuiltinFunctionType,
    types.BuiltinMethodType,
    types.ModuleType,
    types.FileType,
    types.XRangeType,
    types.SliceType,
    types.EllipsisType,
    types.TracebackType,
    types.FrameType,
    types.BufferType,
    types.DictProxyType,
    types.NotImplementedType,
    types.GetSetDescriptorType,
    types.MemberDescriptorType,
    types.StringTypes,
]

def dumps(t):
    if t in type_list:
        return wrap.dumps(type_list.index(t))
    else:
        return class_husky.dumps(t)


def loads(i):
    b = wrap.loads(i)
    if isinstance(b, int):
        return type_list[b]
    else:
        return class_husky.loads(i)