
NODE_LIST = [ 'Module', 'id', 'if', 'setq',
'defun', 'and', 'arxload', 'funcname', '/',
 'strcat', 'cond', 'not', 'progn', 'msg', 'princ',
 'findfile', 'getvar', 'substr', 'getfiled', 'num',
  'repeat', 'while', 'member', 'getstring', 'open',
   'close', '-', 'list', 'fix', '+', 'strlen', 'load',
   'eval', 'equal', 'or', '>', 'itoa', 'cons', 'read',
   'strcase', 'wcmatch', 'type', 'setvar', '>=', '*', '/=',
   '=', 'fp1', 'fp', 'reverse', 'command', 'ssget', 'source',
   'length', 'append', '<', 'vlax', 'mapcar', 'rem', 'nth', 'car',
   'lambda', 'chr', 'null', 'rights',  'lst', 'foreach', 'cdr',
   'initget', 'getkword', 'getint', 'polar', 'sslength', '<=', 'logand',
   'cadr', 'caddr', 'last', 'getreal', 'atoi', 'max', 'entmake', 'prompt',
   'entdel', 'print', 'getpoint', 'entmod', 'entget', 'atof', 'trans', 'getdist',
   'abs', 'distance', 'angle', 'atan', 'sqrt', 'nentsel', 'entsel',
   'ssname', 'assoc', 'subst', 'rtos', 'min', 'ascii', 'sin', 'cos']
print(NODE_LIST)
'''
NODE_LIST = [
    'Module','Interactive','Expression','FunctionDef','ClassDef','Return',
    'Delete','Assign','AugAssign','Print','For','While','If','With','Raise',
    'TryExcept','TryFinally','Assert','Import','ImportFrom','Exec','Global',
    'Expr','Pass','Break','Continue','attributes','BoolOp','BinOp','UnaryOp',
    'Lambda','IfExp','Dict','Set','ListComp','SetComp','DictComp',
    'GeneratorExp','Yield','Compare','Call','Repr','Num','Str','Attribute',
    'Subscript','Name','List','Tuple','Load','Store','Del',
    'AugLoad','AugStore','Param','Ellipsis','Slice','ExtSlice','Index','And','Or',
    'Add','Sub','Mult','Div','Mod','Pow','LShift','RShift','BitOr','BitXor',
    'BitAnd','FloorDiv','Invert','Not','UAdd','USub','Eq','NotEq','Lt',
    'LtE','Gt','GtE','Is','IsNot','In','NotIn','comprehension','ExceptHandler',
    'arguments','keyword','alias','setqgold_cmd',']
'''
NODE_MAP = {x: i for (i, x) in enumerate(NODE_LIST)}
