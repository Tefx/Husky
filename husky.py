import struct
import marshal
import pickle
import types
import ctypes
import czjson as json


class Pickler(object):
	cellnew = ctypes.pythonapi.PyCell_New
	cellnew.restype = ctypes.py_object
	cellnew.argtypes = (ctypes.py_object,)

	dispatch = [
		(types.NoneType, "plain",),
		(types.BooleanType, "plain"),
		(types.IntType, "plain"),
		(types.LongType, "plain"),
		(types.FloatType, "plain"),
		(types.ComplexType, "pickle"),
		(types.StringType, "plain"),
		(types.UnicodeType, "pickle"),
		(types.TupleType, "iterable"),
		(types.ListType, "iterable"),
		(types.DictType, "dict"),
		(types.DictionaryType, "dict"),
		(types.FunctionType, "function"),
		(types.LambdaType, "function"),
		(types.BuiltinFunctionType, "pickle"),
		(types.XRangeType, "pickle"),
		(types.ModuleType, "module"),
		(types.GeneratorType, "iterable"),
		(object, "pickle")
	]

	ignores = ["__file__",
			   "__package__",
			   "__name__",
			   "__doc__",
			   "Husky"]

	def tag(self, s, t):
		return struct.pack(">c", chr(self.dispatch.index(t)))+s

	def untag(self, s):
		return ord(struct.unpack(">c", s)[0])

	def dumps(self, d):
		for item in self.dispatch:
			if isinstance(d, item[0]):
				dumper = getattr(self, "dump_%s" % (item[1],))
				return self.tag(json.dumps(dumper(d)), item)
		return None

	def loads(self, s):
		t, f = self.dispatch[self.untag(s[0])]
		loader = getattr(self, "load_%s" % (f,))
		return loader(json.loads(s[1:]), t)

	def dump_plain(self, d):
		return d

	def load_plain(self, s, t):
		return t(s)

	def dump_iterable(self, d):
		return [self.dumps(x) for x in d]

	def load_iterable(self, s, t):
		if t is types.GeneratorType:
			return [self.loads(x) for x in s]
		else:
			return t(self.loads(x) for x in s)

	def dump_dict(self, d):
		return {self.dumps(k):self.dumps(v) for k,v in d.iteritems()}

	def load_dict(self, s, _):
		return {self.loads(k):self.loads(v) for k,v in s.iteritems()}

	def dump_function(self, f):
		code = pickle.dumps(marshal.dumps(f.func_code))
		if f.func_closure:
			closure = [self.dumps(c.cell_contents) for c in f.func_closure]
		else:
			closure = None
		return code, self.dumps(self.requires(f)), closure
	
	def load_function(self, s, _):
		code, g, closure = s
		g = self.loads(g)
		if closure:
			closure = tuple(self.cellnew(self.loads(c)) for c in closure)
		return types.FunctionType(marshal.loads(pickle.loads(code)), g,
			closure=closure)

	def dump_pickle(self, d):
		return pickle.dumps(d)

	def load_pickle(self, s, _):
		return pickle.loads(s)

	def dump_module(self, d):
		return d.__name__

	def load_module(self, s, _):
		return __import__(s)

	def requires(self, f):
		fg = f.func_globals
		g = {k:v for k,v in fg.iteritems() \
				if (  isinstance(v, types.ModuleType) \
					  or \
					  isinstance(v, types.BuiltinFunctionType))
				   and \
				   k not in self. ignores}
		for k in f.func_code.co_names:
			if k in fg and k != f.func_name:
				g[k] = fg[k]
		return g
		

if __name__ == '__main__':
	p = Pickler()

	def f(x):
		return x+20

	import math

	def g(x):
		return f(x)+id(2)

	a = p.dumps(g)
	g2 = p.loads(a)
	print g2(6)


