# -*- coding:utf-8 -*-
#author xin
from scrapy.cmdline import execute

import sys
import os
from urllib import parse

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(['scrapy','crawl','lagou'])
execute(['scrapy','crawl','jobbole'])
