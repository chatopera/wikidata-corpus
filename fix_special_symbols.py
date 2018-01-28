#!/usr/bin/python
# -*- coding: utf-8 -*-
# python fix_special_symbols.py data/zhwiki-latest-pages-articles.0620.chs
import re
import sys
import codecs


def myfun(input_file):
    p1 = re.compile(ur'-\{.*?(zh-hans|zh-cn):([^;]*?)(;.*?)?\}-')
    p2 = re.compile(ur'[（\(][，；。？！\s]*[）\)]')
    p3 = re.compile(ur'[「『]')
    p4 = re.compile(ur'[」』]')
    outfile = codecs.open(input_file + ".normalized", 'w', 'utf-8')
    with codecs.open(input_file, 'r', 'utf-8') as myfile:
        for line in myfile:
            line = p1.sub(ur'\2', line)
            line = p2.sub(ur'', line)
            line = p3.sub(ur'“', line)
            line = p4.sub(ur'”', line)
            outfile.write(line)
    outfile.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: python fix_special_symbols.py inputfile"
        sys.exit()
    reload(sys)
    sys.setdefaultencoding('utf-8')
    input_file = sys.argv[1]
    myfun(input_file)
