#! /bin/env python
# encoding=utf-8
# gusimiu@baidu.com
# 

import ConfigParser
from tpsr_core import *

class UnitParser(BasicParser):
    ''' 解析数字+单位的tag
        如1.73m、23KG等等
    '''
    def __init__(self, name, config_file):
        BasicParser.__init__(self, name)
        self.__config = ConfigParser.ConfigParser()
        self.__config.read(config_file)
        self.__unit_dict = {}

        encoding=self.__config.get('encoding', 'encoding')

        # 获取标准展示的单位
        self.__standard_unit = self.__config.get(name, 'standard_unit')
        # 获取不同单位信息：
        #   u1_0,u1_1',u1_2,u1_3:trans_num@@unit_2:trans_num@@...
        # 如：
        #   cm,CM,厘米,centimeter:1@@m,M,米,meter:100
        unit_info = self.__config.get(name, 'unit_info')
        for s in unit_info.split('@@'):
            unames, trans_mount = s.split(':')
            trans_mount = float(trans_mount)
            for name in unames.split(','):
                if encoding=='utf-8':
                    name = name.decode('utf-8').encode('gb18030')
                name = name.strip()
                #print '%s: %s' % (name, trans_mount)
                self.__unit_dict[name] = trans_mount

    def find_all(self, text_object):
        text = text_object.text

        num_results = text_object.get('NUM')
        num_result_dict = {}
        temp_ans = []
        for info in num_results:
            num_result_dict[info.begin] = info
            mount = info.value
            span = (info.begin, info.end)
            p = info.end
            while p < len(text):
                if p == ' ':
                    p += 1
                else: 
                    break
            for unit_name, scale in self.__unit_dict.iteritems():
                # 前缀匹配
                if text[p:p+len(unit_name)] == unit_name:
                    mount = mount * scale
                    temp_ans.append( TextSpan(info.begin, p+len(unit_name), mount))
                    break

        # 首先把相连的连在一起
        ans = []
        temp_ans = sorted(temp_ans, key=lambda x:x.sort_key())
        for s in temp_ans:
            if len(ans)==0: ans.append(s)
            else:
                last_ans = ans[len(ans)-1]
                if last_ans.end == s.begin:
                    new_ans = TextSpan(last_ans.begin, s.end, last_ans.value + s.value)
                    ans[len(ans)-1] = new_ans
                else:
                    ans.append(s)

        # 把所有跟着的数字弄进去。
        for s in ans:
            p = s.end
            if p in num_result_dict:
                s.set_value( s.value + num_result_dict[p].value )
            s.set_value( (s.value, self.__standard_unit) )
        
        text_object.set(self.key, ans)
        # debug answers.
        '''
        for s in ans:
            print '[%d,%d] : [[%.3f%s]]' % (s.begin, s.end, s.value, self.__standard_unit)
        '''
            
if __name__=='__main__':
    from num import *
    lpsr = UnitParser('UNIT_LENGTH', 'unit.conf')
    wpsr = UnitParser('UNIT_WEIGHT', 'unit.conf')
    psr = NumParser()

    while 1:
        text = raw_input()
        if text=='': break
        
        to = TextObject(text)
        psr.find_all(to)
        lpsr.find_all(to)
        wpsr.find_all(to)

        ans = to.get('UNIT_LENGTH')
        print 'ABOUT LENGTH:'
        for s in ans:
            print '(%d,%d) : [%f %s]' % (s.begin, s.end, s.value[0], s.value[1]) 

        ans = to.get('UNIT_WEIGHT')
        print 'ABOUT WEIGHT:'
        for s in ans:
            print '(%d,%d) : [%f %s]' % (s.begin, s.end, s.value[0], s.value[1]) 


