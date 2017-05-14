import re




p = u'<total_fee>(?P<amount>\d+)</total_fee>'
pattern = re.compile(ur"%s"%p)
print pattern.search("<total_fee>100</total_fee>").groupdict()
