#!/usr/bin/env python3

#执行指定命令，并判断是否存在期望字符串存在，支持正则表达式
#入口: <command> [<argument>] [...] <pattern> <ignore-case>
#出口： 存在，则输出yes

import sys
import subprocess
import re

agrs = ' '.join(sys.argv[1:-2])
patten = sys.argv[-2]
if sys.argv[-1] == '1':
    flags = re.I
else:
    flags = 0

sp = subprocess.run(agrs, capture_output=True, timeout=60, text=True, shell=True)

result = re.search(patten, sp.stdout, flags)

if result != None:
    print('yes')

