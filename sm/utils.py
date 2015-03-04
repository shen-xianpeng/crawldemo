# -*- coding: utf-8 -*-
from hashlib import md5
import re

num_pattern = re.compile('(\d+)')


def get_nums(text, p=num_pattern):
    matches = p.finditer(text)
    match_nums = [match.groups()[0] for match in matches]
    return int(match_nums[0]) if match_nums else None

def hash_item_fields(item, fields=None):
    ''' 按指定字段哈希抓取的条目 ，生成唯一key 以便对比发现内容是否有更新
              问题是以哪些字段作为生成唯一key的标准
    >>> hash_item_fields({'1':1})
    '52ae16bd2b12ffaf313b9bbd43896495'
    '''
    tmp_item = item.copy()
    for field in item.keys():
        if fields and (field not in fields):
            tmp_item.pop(field, None)
    digester = md5()
    digester.update(tmp_item.__repr__())
    return digester.hexdigest()

import time
def get_format_str(time_float,str_format='%Y年%m月%d日'):
    if time_float:
        return time.strftime(str_format,time.localtime(time_float))
    
    return ''

def get_year_month(time_float):
    ''' '''
    s =  get_format_str(time_float, str_format='%Y-%m')
    return map(int, s.split('-'))


def get_float_datestr(datastr, str_format='%Y-%m-%d %H:%M'):
    return int(time.mktime(time.strptime(datastr,str_format)))

import itertools
import re
start_p = u'((?P<start_year>\d+)年)?[^0-9]*(?P<start_month>\d+)月(?P<start_day>\d+)日[^0-9]*((?P<start_hour>\d+):(?P<start_minute>\d+))?'
end_p = u'((?P<end_year>\d+)年)?(?P<end_month>\d+)月(?P<end_day>\d+)日[^0-9]*((?P<end_hour>\d+):(?P<end_minute>\d+))?'

#itertools.product(start_ps, end_ps)
activity_time_pattern = re.compile(ur"%s.*至[^0-9]*%s"%(start_p, end_p))
apply_time_pattern = re.compile(ur"%s"%start_p)

def convert_str_to_float(to_match_str):
    ''' 日期字符串转时间戳'''
    time_dict = get_apply_date(to_match_str)
    if not time_dict: return None
    return get_timedict_float(time_dict, 'start', guess_current_year=False)

def convert_str_to_float_pair(to_match_str):
    ''' 日期字符串转 时间戳 一对'''
    time_dict = get_activity_date(to_match_str)
    if not time_dict: return None

    print to_match_str
    try:
        data = get_activity_time_float(time_dict)
        return data
    except:
        import traceback
        traceback.print_exc()


def get_timedict_float(timedict, prefix=None, guess_current_year=True):
    assert prefix!=None
    current_time = int(time.time()) ; year, month = get_year_month(current_time)
    key_month = int(timedict.get('%s_month'%prefix))
    key_day = int(timedict.get('%s_day'%prefix))
    key_hour = int(timedict.get('%s_hour'%prefix) or 0)
    key_minute = int(timedict.get('%s_minute'%prefix) or 0)
    key_year = timedict.get('%s_year'%prefix)
    if key_year and len(key_year)==2:
        key_year = '20'+key_year

    if not(guess_current_year) and not(key_year) and key_month<month: #没指定日期 并且日期月份小于当前月份
        key_year = year + 1
    if not key_year: key_year = year
    time_str = "%d-%d-%d %d:%d" % (int(key_year), key_month, key_day, key_hour, key_minute)
    print time_str
    return get_float_datestr(time_str, "%Y-%m-%d %H:%M")

def get_activity_time_float(timedict):
    start = get_timedict_float(timedict, 'start')
    end = get_timedict_float(timedict, 'end', guess_current_year=False)
    return start, end


from BeautifulSoup import BeautifulSoup


regex = ur'(\n){2,}'
pattern = re.compile(regex, re.UNICODE | re.DOTALL | re.IGNORECASE)
def get_visible_text(soup):
    def visible(element):
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
            return False
        elif re.match('<!--.*-->', str(element)):
            return False
        elif not str(element).strip():
            return False
        return True
    texts = soup.findAll(text=True)
    visible_texts = filter(visible, texts)
    text = '\n'.join((i.strip() for i in visible_texts))
    page_images = [image["src"] for image in soup.findAll("img")]
    return pattern.sub('\n', text)


def replace_true_src(body, img_attr=''):
    assert img_attr
    #non greedy find
    pattern_img_src = re.compile(ur'<img(.*?)src="(.*?)".*?%s="(.*?)"(.*?)>'%img_attr, re.UNICODE | re.DOTALL | re.IGNORECASE)
    return pattern_img_src.sub(r'<img\g<1>src="\g<3>" \g<4>>', body)

age_range_p = re.compile(ur'(?P<age_start>\d+(\.\d+)?)[^0-9]+(?P<age_end>\d+(\.\d+)?)')
age_up_p = re.compile(ur'(?P<age_up>\d+(\.\d+)?)[^0-9]*上')
def get_age_range(age_range_str):
    match = age_up_p.search(age_range_str) if age_range_str else None
    if match:
        return match.groupdict()
    print 'retry'
    match = age_range_p.search(age_range_str) if age_range_str else None
    if match: return match.groupdict()



if __name__ == "__main__":
    import doctest
    doctest.testmod()
