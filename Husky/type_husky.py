import wrap
import types

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
    object
]

def dumps(t):
    return wrap.dumps(type_list.index(t))

def loads(i):
    return type_list[wrap.loads(i)]