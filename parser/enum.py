#! /bin/env python
# encoding=utf-8
# gusimiu@baidu.com
# 

from tpsr_core import *
from trie import *

class EnumParser(BasicParser):
    def __init__(self, dictfile):
        BasicParser.__init__(self, 'ENUM')
        self.__trie = Trie()
        for l in file(dictfile).readlines():
            word_list = l.strip().split('\t')
            norm_output = word_list[0]
            for w in word_list:
                self.__trie.insert(w, norm_output)

    def find_all(self, text_object):
