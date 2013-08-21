#! /bin/env python
# encoding=utf-8
# gusimiu@baidu.com
# 

import sys
import text_object
import basic_tparser

class TParser:
    def __init__(self):
        pass

    def parse(self, concept, text):
        tobj = text_object.TextObject(text)
        self.__build_dependence(concept)
        for conc in self.__concept_order:
            conc.parse(tobj)
        concept.parse(tobj)
        return concept.build_output(tobj)

    def __build_dependence(self, concept):
        self.__concept_order = []
        self.__concept_order.append(concept)
        dep_set = set()
        for con in self.__concept_order:
            psr = self.__get_parser(con)
            if psr is None:
                raise Exception('Cannot find parser [[ %s ]]' % con)
            for dep in psr.dependence():
                if dep in dep_set:
                    continue
                dep_set.add(dep)
                self.__concept_order.append(dep)

if __name__=='__main__':
    concept = 'NUM'
    psr = TParser()
    while 1:
        text = sys.stdin.readline()
        if text == '': break
        text = text.strip()
        psr_out = psr.parse(concept, text)
        psr_out.debug()
