#! /bin/env python
# encoding=utf-8
# gusimiu@baidu.com
# 

from tpsr_core import *
from trie import *

class EnumParser(BasicParser):
    def __init__(self, name, dictfile):
        BasicParser.__init__(self, name)
        self.__trie = Trie()
        for l in file(dictfile).readlines():
            word_list = l.strip().split('\t')
            norm_output = word_list[0]
            for w in word_list:
                self.__trie.insert(w, norm_output)
        self.__trie.end_insert()

    def find_all(self, text_object):
        text = text_object.text
        ans = []
        for pos, s, info in self.__trie.find(text):
            ans.append( TextSpan(pos, pos+len(s), info) )
        ans = sort_text_span(ans)
        final_ans = []
        for i in range(0, len(ans)-1):
            if i>0 and is_A_in_B(ans[i], ans[i-1]):
                continue
            else:
                final_ans.append( ans[i] )
        text_object.set(self.key, final_ans)

if __name__=='__main__':
    constell_parser = EnumParser('ENUM_CONSTELL', 'dict/constellation.txt')
    while 1:
        text = raw_input()
        to = TextObject(text)
        constell_parser.find_all(to)
        for span in to.get('ENUM_CONSTELL'):
            print '[%s,%s] %s: %s' % (span.begin, 
                    span.end, text[span.begin:span.end], span.value)


