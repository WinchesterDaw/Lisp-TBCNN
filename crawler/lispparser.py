from cmath import pi
from encodings import utf_8
import sys
import types
import os

from typing import Any, List

func_name = set()
# Generate abstract syntax tree from normalized input.
def get_ast(input_norm: List[str]) -> List[Any]:
    ast = []
    i = 0
    while i < len(input_norm):
        symbol = input_norm[i]
        if symbol == '(':
            list_content = []
            match_ctr = 1 # If 0, parenthesis has been matched.
            while match_ctr != 0:
                #print(symbol)
                i += 1
                if i >= len(input_norm):
                    break
                    #raise ValueError("Invalid input: Unmatched open parenthesis.")
                symbol = input_norm[i]
                if symbol == '(':
                    match_ctr += 1
                elif symbol == ')':
                    match_ctr -= 1
                if match_ctr != 0:
                    list_content.append(symbol)
            ast.append(get_ast(list_content))
        elif symbol == ')':
            i+=1
            continue
            #raise ValueError("Invalid input: Unmatched close parenthesis.")
        else:
            try:
                ast.append(int(symbol))
            except ValueError:
                ast.append(symbol)
        i += 1
    return ast

keyword=[ 'id', 'if', 'setq', 
'defun', 'and', 'arxload', 'funcname', '/',
 'strcat', 'cond', 'not', 'progn', 'msg', 'princ', 
 'findfile', 'getvar', 'substr', 'getfiled', 'num',
  'repeat', 'while', 'member', 'getstring', 'open',
   'close', '-', 'list', 'fix', '+', 'strlen', 'load', 
   'eval', 'equal', 'or', '>', 'itoa', 'cons', 'read', 
   'strcase', 'wcmatch', 'type', 'setvar', '>=', '*', '/=', 
   '=', 'fp1', 'fp', 'reverse', 'command', 'ssget', 'source', 
   'length', 'append', '<', 'vlax', 'mapcar', 'rem', 'nth', 'car', 
   'lambda', 'chr', 'null', 'rights', 'foreach', 'cdr', 
   'initget', 'getkword', 'getint', 'polar', 'sslength', '<=', 'logand', 
   'cadr', 'caddr', 'last', 'getreal', 'atoi', 'max', 'entmake', 'prompt', 
   'entdel', 'print', 'getpoint', 'entmod', 'entget', 'atof', 'trans', 'getdist', 
   'abs', 'distance', 'angle', 'atan', 'sqrt', 'nentsel', 'entsel', 
   'ssname', 'assoc', 'subst', 'rtos', 'min', 'ascii', 'sin', 'cos']

def whichtype(symbol,first=False):
    if isinstance(symbol,list):
        return 'funcname'
    if first:
        #if len(str(symbol))>=10 or "_" in str(symbol):
        if isinstance(symbol,list):
            return 'funcname'
        if ":" in str(symbol):
            if "::" in str(symbol):
                symbol=symbol.split("::")[-1]
            else:
                symbol=symbol.split(":")[-1]
        if "-" in str(symbol) and str(symbol)!="-" and str(symbol)[0]!='-':
            symbol=symbol.split("-")[-1]
        if str(symbol) in keyword:
            return symbol
        else:
            return "funcname"
            '''
        with open("C:/Users/71465/Desktop/paper/new/tbcnn-ast/crawler/symbol", 'a+',encoding='gbk') as f:
            sy=f.read()
            flag=True
            for line in sy:
                if line==symbol:
                    flag=False
                    break
            if flag:
                f.write("\n"+str(symbol))'''
    elif type(symbol)==int or type(symbol)==float:
        return 'num'
    elif symbol[0] == '"' and symbol[-1] == '"':
        return 'str'
    else:
        return 'id'


def build_tree(ast,pa="None"):
    if not isinstance(ast,list):
        return {
            'name':whichtype(ast),
            'child':[]
        }
    if len(ast) <= 0:
        return []
    tree_info ={
        'name' : whichtype(ast[0],True) if len(ast)>1 else whichtype(ast[0]),
        'parent' : pa,
        'child' : []
    }

    for item in ast[1:]:
        i = build_tree(item,tree_info['name'])
        if i==[]:
            continue
        i['parent'] = tree_info['name']
        tree_info['child'].append(i)
        '''
    if tree_info['name']=="defun":
        func_name.add(tree_info['child'][0]['name'])
        tree_info['child'][0]['name']="funcname"'''
    #print(tree_info)
    return tree_info


def main():

    # path = "C:/Users/71465/Desktop/paper/new/tbcnn-ast/crawler/code_sample/lsp"
    path = "C:/Users/71465/Desktop/paper/new/tbcnn-ast/crawler/code_sample/good"
    all_file = []
    index=0
    for f in os.listdir(path):  #listdir返回文件中所有目录
        #os.rename(os.path.join(path, f), os.path.join(path, str(index)))
        #f_name = os.path.join(path, str(index))
        f_name = os.path.join(path, f)
        all_file.append(f_name)
        index+=1
    ii=0

    for name in all_file:
    #with open(all_file[0], 'r') as f:
        print(name)
        ii= ii+1
        instr = False
        with open(name, 'rb') as f:
            input_str=f.read().decode('utf-8','ignore')
        ans = ""
        zhushi = 0
        for i in input_str:
            if i == '\n':
                zhushi=0
            elif zhushi==1:
                continue
            elif (i =='(' ) | ( i==")"):
                ans = ans+" "+i+" "
            elif i==';':
                zhushi=0
            elif i == ' ':
                if not instr:
                    ans+=i
            elif i == '"':
                instr = not instr
            elif i == "'":
                continue
            else:
                ans+=str(i).lower()
        input_str = ans
        input_str = input_str.split()
        fun = False
        """Traverse a tree and execute the callback on every node."""

        queue = [input_str]
        while queue:
            current_node = queue.pop(0)
            if fun:
                fun=False
                if ":" in str(current_node):
                    if "::" in str(current_node):
                        current_node=current_node.split("::")[1]
                    else:
                        current_node=current_node.split(":")[1]
                    if "-" in str(current_node) and str(current_node)!="-":
                        current_node=current_node.split("-")[0]
                func_name.add(current_node)
            if current_node == "defun":
                fun=True
            if isinstance(current_node,list):
                queue.extend(current_node)

        try:
            
            print("func_name=",func_name)
            ast = get_ast(input_str)
            ans ={
            'name' : "Module",
            'parent' : "None",
            'child' : [build_tree(i,"Module") for i in ast]
            }
            with open("C:/Users/71465/Desktop/paper/new/tbcnn-ast/crawler/code_sample/ast_good/"+name.split("\\")[-1]+"_ast", 'a+') as f:
                f.write(str(ans))
        except ValueError:
            print("error",name)
    print("end")

if __name__ == '__main__':
    main()