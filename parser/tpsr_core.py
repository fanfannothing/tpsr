#! /bin/env python
# encoding=utf-8
# gusimiu@baidu.com
# 

import logging

class TextSpan(object):
    def __init__(self, beg, end, value): 
        self.__begin = beg
        self.__end = end
        self.__value = value
    @property
    def begin(self): return self.__begin
    @property
    def end(self): return self.__end
    @property
    def value(self): return self.__value
    
    def set_value(self, new_val): self.__value = new_val

    def sort_key(self): 
        return (self.__begin, -self.__end)

class TextObject(object):
    def __init__(self, text):
        self.__text = text
        self.__output_span = {}

    def set(self, key, span_list):
        ''' 设置一个span列表，如果已经存在，
        报警&替换
        '''
        if key in self.__output_span:
            logging.warning('SpanExists: key=[%s]' % key)
        self.__output_span[key] = span_list

    def get(self, key):
        ''' 返回特定key下面的span结果
        '''
        return self.__output_span.get(key, [])

    @property
    def text(self): return self.__text

class BasicParser(object):
    def __init__(self, key): 
        self.__key = key

    @property
    def key(self): return self.__key

