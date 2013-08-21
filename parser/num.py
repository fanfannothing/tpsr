#! /bin/env python
# encoding=utf-8
# gusimiu@baidu.com
# 

import re

from tpsr_core import *

class NumParser(BasicParser):
    def __init__(self):
        BasicParser.__init__(self, 'NUM')
        self.__num_pattern = re.compile('[+-]{0,1}[0-9]+(\.[0-9]+){0,1}')
        self.__num_pattern_with_comma = re.compile('[+-]{0,1}([0-9]{3},){,}[0-9]{3}(\.[0-9]+){0,1}')

    def find_all(self, text_object):
        text = text_object.text
        spans = []
        temp_spans = []
        for m in self.__num_pattern.finditer(text):
            temp_spans.append( (m.span(), m.group()) )
        for m in self.__num_pattern_with_comma.finditer(text):
            temp_spans.append( (m.span(), m.group()) )
        temp_spans = sorted(temp_spans, key=lambda x:(x[0][0], -x[0][1]))
        if len(temp_spans)>0:
            spans.append(temp_spans[0])
            for i in range(1, len(temp_spans)):
                my_span = temp_spans[i][0]
                last_span = spans[-1][0]
                if my_span[0]>=last_span[0] and my_span[1]<=last_span[1]:
                    # ignore span which is in last span.
                    continue
                spans.append( temp_spans[i] )
        # make answer list.
        ans = []
        for s in spans:
            sp = TextSpan(s[0][0], s[0][1], float(s[1]) )
            ans.append(sp)
        text_object.set(self.key, ans) 

if __name__=='__main__':
    psr = NumParser()
    while 1:
        text = raw_input()
        if text=='': break
        
        to = TextObject(text)
        psr.find_all(to)

        ans = to.get('NUM')
        for s in ans:
            print '(%d,%d) : [%f]' % (s.begin, s.end, s.value) 
    
