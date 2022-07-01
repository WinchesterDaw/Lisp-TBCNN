"""
This script scrapes files from GitHub with specific algorithm purposes, and
labels them by the algorithm

Labels are:
    bubblesort
    mergesort
    quicksort
    linkedlist
    bfs (breadth first search)
    knapsack
"""

import os
import sys
import ast
import logging
import pickle
import json
import crawler.utils as utils

from collections import defaultdict
from crawler.algorithms.constants import CACHE_DIR, REQUESTS_CACHE

DATA_URLS = {
    'test1': ['a=123\nprint("123")',
              'b=123\nprint("123")'],
    'test2': ['a=123\na=a*a\n'
              'a=123\na=a*a*a\n'],
}

def build_tree(script):
    """Builds an AST from a script."""
    return ast.parse(script)

def fetch(outfile):
    """The main function for downloading all scripts from github."""
    if not os.path.exists(REQUESTS_CACHE):
        os.makedirs(REQUESTS_CACHE)


    result = []

    label_counts = defaultdict(int)
    sys.setrecursionlimit(3000)
    print('Fetching scripts')
    for [path,label] in [["C:/Users/71465/Desktop/paper/new/tbcnn-ast/crawler/code_sample/ast",
                        "marvel"],
                       ["C:/Users/71465/Desktop/paper/new/tbcnn-ast/crawler/code_sample/ast_good",
                        "good"]]:
    #path = "C:/Users/71465/Desktop/paper/new/tbcnn-ast/crawler/code_sample/ast"
        all_file=[]
        data_source=[]
        for f in os.listdir(path):
            f_name = os.path.join(path, f)
            all_file.append(f_name)
        for name in all_file:
            with open(name, 'r') as f:
                input_str = f.read()
                print(name)
                data = json.loads(input_str.replace("'", '"'))
                data['parent'] = None
                data_source.append({'tree': data, 'metadata': {'label': label}})
        for script in data_source:
            result.append(script)
            label_counts[label] += 1
    print('Label counts: ', label_counts)

    print('Dumping scripts')
    with open(outfile, 'wb') as file_handler:
        pickle.dump(result, file_handler)
