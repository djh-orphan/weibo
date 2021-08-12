import re

# line='2021-08-03 15:29:02.069446+08:00'
# rer=''
# matchobj=re.match(r'(\d{4})-(\d{2})-(\d{2})\s(\d{2}):(\d{2}):(\d{2}).*',line,re.M|re.I)
# aa=matchobj.groups()
# map(lambda x:int(x),aa)
# ab=[list(map(lambda x:int(x),aa[0:3])),list(map(lambda x:int(x),aa[3:6]))]

ab={"id":123,"username":222}
ab.pop('info',None)
print(ab)
